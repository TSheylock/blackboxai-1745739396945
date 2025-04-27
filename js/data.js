// Sample Knowledge Graph Data
const graphData = {
    nodes: [
        // Emotion Nodes
        { data: { id: 'trust', label: 'Trust', type: 'emotion', color: '#10B981' } },
        { data: { id: 'fear', label: 'Fear', type: 'emotion', color: '#EF4444' } },
        { data: { id: 'joy', label: 'Joy', type: 'emotion', color: '#F59E0B' } },
        
        // Concept Nodes
        { data: { id: 'healing', label: 'Healing', type: 'concept', color: '#8B5CF6' } },
        { data: { id: 'connection', label: 'Connection', type: 'concept', color: '#8B5CF6' } },
        
        // Memory Nodes
        { data: { id: 'memory1', label: 'First Interaction', type: 'memory', color: '#3B82F6' } },
        { data: { id: 'memory2', label: 'Learning Experience', type: 'memory', color: '#3B82F6' } }
    ],
    edges: [
        // Relationships
        { data: { source: 'trust', target: 'healing', label: 'enables' } },
        { data: { source: 'fear', target: 'connection', label: 'blocks' } },
        { data: { source: 'joy', target: 'connection', label: 'strengthens' } },
        { data: { source: 'memory1', target: 'trust', label: 'created' } },
        { data: { source: 'memory2', target: 'healing', label: 'reinforced' } }
    ]
};
