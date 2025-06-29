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

// Route to serve the main HTML file
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Chat endpoint that communicates with Python Meta AI script
app.post('/api/chat', async (req, res) => {
    try {
        const { message } = req.body;
        
        if (!message || message.trim() === '') {
            return res.status(400).json({ error: 'Message is required' });
        }

        // Add user message to history
        conversationHistory.push({ role: 'user', content: message, timestamp: new Date() });

        // Create a Python process to handle the Meta AI request
        const pythonProcess = spawn('python3', ['-c', `
import sys
sys.path.append('.')
from meta_ai_api import MetaAI
import json

try:
    ai = MetaAI()
    user_message = "${message.replace(/"/g, '\\"')}"
    response = ai.prompt(message=user_message)
    
    if isinstance(response, dict):
        cleaned_response = str(response.get('message', ''))
    else:
        cleaned_response = str(response).replace("\\n", " ")
    
    cleaned_response = cleaned_response.replace("source:", "").replace("media:", "").strip()
    print(json.dumps({"success": True, "response": cleaned_response}))
    
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
                if (code === 0 && pythonOutput.trim()) {
                    const result = JSON.parse(pythonOutput.trim());
                    
                    if (result.success) {
                        const aiResponse = result.response || "I'm sorry, I couldn't generate a response.";
                        
                        // Add AI response to history
                        conversationHistory.push({ 
                            role: 'assistant', 
                            content: aiResponse, 
                            timestamp: new Date() 
                        });

                        res.json({ 
                            success: true, 
                            response: aiResponse,
                            timestamp: new Date().toISOString()
                        });
                    } else {
                        throw new Error(result.error || 'Unknown error from Python script');
                    }
                } else {
                    throw new Error(pythonError || 'Python script failed to execute');
                }
            } catch (error) {
                console.error('Error processing Python response:', error);
                res.status(500).json({ 
                    success: false, 
                    error: 'Failed to get response from AI. Please make sure meta_ai_api is installed.',
                    details: error.message
                });
            }
        });

    } catch (error) {
        console.error('Server error:', error);
        res.status(500).json({ 
            success: false, 
            error: 'Internal server error',
            details: error.message
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
    console.log(`🤖 Make sure you have installed: pip install meta_ai_api`);
});