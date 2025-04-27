import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import logging
from typing import Dict, Optional, Tuple
import base64
import io
from PIL import Image

class EmotionDetector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.model = None
        self.initialize_model()

    def initialize_model(self):
        """Initialize the emotion detection model"""
        try:
            # In production, replace with path to your trained model
            self.model = load_model('models/emotion_model.h5')
            self.logger.info("Emotion detection model loaded successfully")
        except Exception as e:
            self.logger.error(f"Error loading emotion detection model: {str(e)}")
            raise

    async def process_image(self, image_data: str) -> Dict:
        """
        Process base64 encoded image data and detect emotions
        """
        try:
            # Decode base64 image
            image_bytes = base64.b64decode(image_data.split(',')[1] if ',' in image_data else image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to OpenCV format
            image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Detect faces
            faces = self.detect_faces(image_cv)
            
            if not faces:
                return {
                    "success": False,
                    "error": "No faces detected in the image"
                }

            # Process each face
            results = []
            for face in faces:
                emotion_data = self.analyze_face(image_cv, face)
                results.append(emotion_data)

            return {
                "success": True,
                "faces_detected": len(faces),
                "results": results
            }

        except Exception as e:
            self.logger.error(f"Error processing image: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    def detect_faces(self, image: np.ndarray) -> list:
        """
        Detect faces in the image using OpenCV
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        return faces

    def analyze_face(self, image: np.ndarray, face: Tuple) -> Dict:
        """
        Analyze emotions for a detected face
        """
        try:
            x, y, w, h = face
            roi_gray = cv2.cvtColor(image[y:y+h, x:x+w], cv2.COLOR_BGR2GRAY)
            roi_gray = cv2.resize(roi_gray, (48, 48))
            roi = roi_gray.astype('float') / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            # Predict emotion
            prediction = self.model.predict(roi)[0]
            emotion_probabilities = {
                emotion: float(prob) 
                for emotion, prob in zip(self.emotions, prediction)
            }
            
            # Get the emotion with highest probability
            max_emotion = max(emotion_probabilities.items(), key=lambda x: x[1])

            return {
                "emotion": max_emotion[0],
                "confidence": max_emotion[1],
                "all_emotions": emotion_probabilities,
                "face_location": {
                    "x": int(x),
                    "y": int(y),
                    "width": int(w),
                    "height": int(h)
                }
            }

        except Exception as e:
            self.logger.error(f"Error analyzing face: {str(e)}")
            return {
                "error": str(e)
            }

    async def process_video_frame(self, frame: np.ndarray) -> Dict:
        """
        Process a single video frame for emotion detection
        """
        try:
            faces = self.detect_faces(frame)
            
            if not faces:
                return {
                    "success": False,
                    "error": "No faces detected in frame"
                }

            results = []
            for face in faces:
                emotion_data = self.analyze_face(frame, face)
                results.append(emotion_data)

            return {
                "success": True,
                "faces_detected": len(faces),
                "results": results
            }

        except Exception as e:
            self.logger.error(f"Error processing video frame: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    def draw_results(self, image: np.ndarray, results: Dict) -> np.ndarray:
        """
        Draw emotion detection results on the image
        """
        try:
            if not results["success"]:
                return image

            for result in results["results"]:
                if "error" in result:
                    continue

                face_loc = result["face_location"]
                emotion = result["emotion"]
                confidence = result["confidence"]

                # Draw rectangle around face
                cv2.rectangle(
                    image,
                    (face_loc["x"], face_loc["y"]),
                    (face_loc["x"] + face_loc["width"], face_loc["y"] + face_loc["height"]),
                    (0, 255, 0),
                    2
                )

                # Draw emotion label
                label = f"{emotion}: {confidence:.2f}"
                cv2.putText(
                    image,
                    label,
                    (face_loc["x"], face_loc["y"] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.45,
                    (0, 255, 0),
                    2
                )

            return image

        except Exception as e:
            self.logger.error(f"Error drawing results: {str(e)}")
            return image

    def get_model_info(self) -> Dict:
        """
        Get information about the emotion detection model
        """
        return {
            "emotions_supported": self.emotions,
            "model_loaded": self.model is not None,
            "input_shape": self.model.input_shape if self.model else None,
            "version": "1.0.0"
        }
