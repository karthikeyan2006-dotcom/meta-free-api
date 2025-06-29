const express = require('express');
const cors = require('cors');
const path = require('path');
const { spawn } = require('child_process');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Store conversation history
let conversationHistory = [];

// Mock AI responses for when meta_ai_api is not available
const mockAIResponses = [
    "I understand your question. While I'm currently running in a limited environment, I'd be happy to help you with general information and conversation.",
    "That's an interesting point! I'm here to assist you with various topics and questions you might have.",
    "I appreciate you reaching out. Even though I'm in a demo mode right now, I can still provide helpful responses and engage in meaningful conversation.",
    "Great question! I'm designed to be helpful, informative, and engaging. What specific topic would you like to explore?",
    "I'm here to help! While my current setup is simplified, I can still assist with information, answer questions, and have conversations.",
    "Thank you for your message. I'm operating in a demonstration mode, but I'm still capable of providing useful responses and assistance."
];

function getMockResponse(message) {
    // Simple response logic based on message content
    const lowerMessage = message.toLowerCase();
    
    if (lowerMessage.includes('joke')) {
        return "Here's a programming joke for you: Why do programmers prefer dark mode? Because light attracts bugs! 😄";
    } else if (lowerMessage.includes('what can you do')) {
        return "I can help with conversations, answer questions, provide information on various topics, assist with problem-solving, and much more! What would you like to explore?";
    } else if (lowerMessage.includes('help')) {
        return "I'm here to help! You can ask me about various topics, request information, get assistance with problems, or just have a friendly conversation. What do you need help with?";
    } else if (lowerMessage.includes('coding') || lowerMessage.includes('programming')) {
        return "I'd be happy to help with coding! I can assist with various programming languages, debugging, best practices, and explaining concepts. What programming topic interests you?";
    } else if (lowerMessage.includes('hello') || lowerMessage.includes('hi')) {
        return "Hello! It's great to meet you. I'm here and ready to help with whatever you need. How can I assist you today?";
    } else {
        // Return a random response from the mock responses array
        return mockAIResponses[Math.floor(Math.random() * mockAIResponses.length)];
    }
}

// Route to serve the main HTML file
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Chat endpoint that tries Meta AI first, falls back to mock responses
app.post('/api/chat', async (req, res) => {
    try {
        const { message } = req.body;
        
        if (!message || message.trim() === '') {
            return res.status(400).json({ error: 'Message is required' });
        }

        // Add user message to history
        conversationHistory.push({ role: 'user', content: message, timestamp: new Date() });

        // Try to use Meta AI first
        const pythonProcess = spawn('python3', ['-c', `
import sys
import json

try:
    # Try to import meta_ai_api
    from meta_ai_api import MetaAI
    
    ai = MetaAI()
    user_message = "${message.replace(/"/g, '\\"')}"
    response = ai.prompt(message=user_message)
    
    if isinstance(response, dict):
        cleaned_response = str(response.get('message', ''))
    else:
        cleaned_response = str(response).replace("\\n", " ")
    
    cleaned_response = cleaned_response.replace("source:", "").replace("media:", "").strip()
    print(json.dumps({"success": True, "response": cleaned_response, "source": "meta_ai"}))
    
except ImportError:
    # meta_ai_api not available, signal to use mock response
    print(json.dumps({"success": False, "error": "meta_ai_api_not_available"}))
    
except Exception as e:
    print(json.dumps({"success": False, "error": str(e)}))
`]);

        let pythonOutput = '';
        let pythonError = '';

        pythonProcess.stdout.on('data', (data) => {
            pythonOutput += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
            pythonError += data.toString();
        });

        pythonProcess.on('close', (code) => {
            try {
                let aiResponse;
                let responseSource = "mock";

                if (code === 0 && pythonOutput.trim()) {
                    const result = JSON.parse(pythonOutput.trim());
                    
                    if (result.success && result.source === "meta_ai") {
                        aiResponse = result.response || "I'm sorry, I couldn't generate a response.";
                        responseSource = "meta_ai";
                    } else {
                        // Use mock response
                        aiResponse = getMockResponse(message);
                    }
                } else {
                    // Use mock response
                    aiResponse = getMockResponse(message);
                }

                // Add AI response to history
                conversationHistory.push({ 
                    role: 'assistant', 
                    content: aiResponse, 
                    timestamp: new Date(),
                    source: responseSource
                });

                res.json({ 
                    success: true, 
                    response: aiResponse,
                    source: responseSource,
                    timestamp: new Date().toISOString()
                });

            } catch (error) {
                console.error('Error processing response:', error);
                
                // Fallback to mock response
                const aiResponse = getMockResponse(message);
                
                conversationHistory.push({ 
                    role: 'assistant', 
                    content: aiResponse, 
                    timestamp: new Date(),
                    source: "mock"
                });

                res.json({ 
                    success: true, 
                    response: aiResponse,
                    source: "mock",
                    timestamp: new Date().toISOString()
                });
            }
        });

    } catch (error) {
        console.error('Server error:', error);
        
        // Fallback to mock response even on server error
        const aiResponse = getMockResponse(req.body.message || "Hello");
        
        conversationHistory.push({ 
            role: 'assistant', 
            content: aiResponse, 
            timestamp: new Date(),
            source: "mock"
        });

        res.json({ 
            success: true, 
            response: aiResponse,
            source: "mock",
            timestamp: new Date().toISOString()
        });
    }
});

// Get conversation history
app.get('/api/history', (req, res) => {
    res.json({ history: conversationHistory });
});

// Clear conversation history
app.delete('/api/history', (req, res) => {
    conversationHistory = [];
    res.json({ success: true, message: 'History cleared' });
});

// Health check endpoint
app.get('/api/health', (req, res) => {
    res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

app.listen(PORT, () => {
    console.log(`🚀 Meta AI Chatbot Server running on http://localhost:${PORT}`);
    console.log(`📱 Open your browser and navigate to http://localhost:${PORT}`);
    console.log(`🤖 Note: Running in demo mode. For full Meta AI integration, install: pip install meta_ai_api`);
});