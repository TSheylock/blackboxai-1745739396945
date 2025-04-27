from .emotion_detector import EmotionDetector
from .nlp_processor import NLPProcessor
from .learning_system import LearningSystem
import logging
from typing import Dict, List, Optional
from datetime import datetime
import asyncio

class AIManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.emotion_detector = None
        self.nlp_processor = None
        self.learning_system = None
        self.initialize_components()

    def initialize_components(self):
        """Initialize all AI components"""
        try:
            self.emotion_detector = EmotionDetector()
            self.nlp_processor = NLPProcessor()
            self.learning_system = LearningSystem()
            self.logger.info("AI components initialized successfully")
        except Exception as e:
            self.logger.error(f"Error initializing AI components: {str(e)}")
            raise

    async def process_input(self, 
                          input_data: Dict,
                          context: Optional[List[Dict]] = None) -> Dict:
        """Process input data through appropriate AI components"""
        try:
            input_type = input_data.get('type', 'text')
            
            if input_type == 'image':
                result = await self.process_image(input_data['data'])
            elif input_type == 'text':
                result = await self.process_text(input_data['data'], context)
            elif input_type == 'video_frame':
                result = await self.process_video_frame(input_data['data'])
            else:
                raise ValueError(f"Unsupported input type: {input_type}")

            # Log interaction for learning
            await self.log_interaction({
                'input_type': input_type,
                'input_data': input_data,
                'result': result,
                'timestamp': datetime.utcnow().isoformat()
            })

            return result

        except Exception as e:
            self.logger.error(f"Error processing input: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    async def process_image(self, image_data: str) -> Dict:
        """Process image data for emotion detection"""
        try:
            emotion_result = await self.emotion_detector.process_image(image_data)
            
            # Enhance result with NLP analysis if text is present
            if 'text' in emotion_result:
                nlp_result = await self.nlp_processor.process_text(emotion_result['text'])
                emotion_result['nlp_analysis'] = nlp_result

            return emotion_result

        except Exception as e:
            self.logger.error(f"Error processing image: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    async def process_text(self, 
                          text: str,
                          context: Optional[List[Dict]] = None) -> Dict:
        """Process text input through NLP pipeline"""
        try:
            # Process text through NLP pipeline
            nlp_result = await self.nlp_processor.process_text(text, context)
            
            # Generate response
            response = await self.nlp_processor.generate_response(text, context)
            
            return {
                'success': True,
                'nlp_analysis': nlp_result,
                'response': response,
                'timestamp': datetime.utcnow().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Error processing text: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    async def process_video_frame(self, frame_data: str) -> Dict:
        """Process video frame for emotion detection"""
        try:
            return await self.emotion_detector.process_video_frame(frame_data)
        except Exception as e:
            self.logger.error(f"Error processing video frame: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    async def log_interaction(self, interaction_data: Dict) -> Dict:
        """Log interaction for learning purposes"""
        try:
            return await self.learning_system.log_interaction(interaction_data)
        except Exception as e:
            self.logger.error(f"Error logging interaction: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    async def train_models(self) -> Dict:
        """Trigger model training based on collected data"""
        try:
            training_results = {}
            
            # Train emotion detection model
            emotion_result = await self.learning_system.train_models('emotion_detection')
            training_results['emotion_detection'] = emotion_result
            
            # Train NLP model
            nlp_result = await self.learning_system.train_models('nlp_processing')
            training_results['nlp_processing'] = nlp_result

            return {
                'success': True,
                'results': training_results,
                'timestamp': datetime.utcnow().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Error training models: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    async def get_system_status(self) -> Dict:
        """Get status of all AI components"""
        try:
            emotion_info = self.emotion_detector.get_model_info()
            nlp_info = self.nlp_processor.get_model_info()
            learning_stats = await self.learning_system.get_learning_stats()

            return {
                'success': True,
                'components': {
                    'emotion_detector': emotion_info,
                    'nlp_processor': nlp_info,
                    'learning_system': learning_stats
                },
                'status': 'operational',
                'last_updated': datetime.utcnow().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Error getting system status: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'status': 'error'
            }

    async def process_feedback(self, feedback_data: Dict) -> Dict:
        """Process user feedback for model improvement"""
        try:
            # Log feedback
            await self.log_interaction({
                'type': 'feedback',
                'data': feedback_data,
                'timestamp': datetime.utcnow().isoformat()
            })

            # Update training data
            await self.learning_system.update_training_data(feedback_data)

            return {
                'success': True,
                'message': 'Feedback processed successfully'
            }

        except Exception as e:
            self.logger.error(f"Error processing feedback: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
