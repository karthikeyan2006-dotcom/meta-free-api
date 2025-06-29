from flask import Flask, render_template_string, request, jsonify
from meta_ai_api import MetaAI
import threading
import webbrowser
import time

app = Flask(__name__)

# Initialize Meta AI
ai = MetaAI()

# HTML template (your chatbot interface)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KARTHIKEYAN'S AI</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .chatbot-container {
            width: 400px;
            height: 600px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        .chat-header {
            background: linear-gradient(135deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3);
            background-size: 300% 300%;
            animation: gradientShift 3s ease infinite;
            padding: 20px;
            text-align: center;
            color: white;
            position: relative;
        }

        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .bot-avatar {
            width: 60px;
            height: 60px;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            border-radius: 50%;
            margin: 0 auto 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }

        .bot-name {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .bot-status {
            font-size: 12px;
            opacity: 0.9;
        }

        .chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .message {
            max-width: 80%;
            padding: 12px 16px;
            border-radius: 18px;
            animation: messageSlide 0.3s ease-out;
        }

        @keyframes messageSlide {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .user-message {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            align-self: flex-end;
            border-bottom-right-radius: 5px;
        }

        .bot-message {
            background: linear-gradient(135deg, #ffecd2, #fcb69f);
            color: #333;
            align-self: flex-start;
            border-bottom-left-radius: 5px;
        }

        .typing-indicator {
            display: none;
            align-self: flex-start;
            background: #f0f0f0;
            padding: 12px 16px;
            border-radius: 18px;
            border-bottom-left-radius: 5px;
        }

        .typing-dots {
            display: flex;
            gap: 4px;
        }

        .dot {
            width: 8px;
            height: 8px;
            background: #999;
            border-radius: 50%;
            animation: typing 1.4s infinite ease-in-out;
        }

        .dot:nth-child(1) { animation-delay: -0.32s; }
        .dot:nth-child(2) { animation-delay: -0.16s; }

        @keyframes typing {
            0%, 80%, 100% {
                transform: scale(0);
                opacity: 0.5;
            }
            40% {
                transform: scale(1);
                opacity: 1;
            }
        }

        .chat-input-container {
            padding: 20px;
            background: white;
            border-top: 1px solid #eee;
        }

        .input-wrapper {
            display: flex;
            gap: 10px;
            align-items: center;
            background: #f8f9fa;
            border-radius: 25px;
            padding: 5px;
            border: 2px solid transparent;
            transition: all 0.3s ease;
        }

        .input-wrapper:focus-within {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .chat-input {
            flex: 1;
            border: none;
            outline: none;
            padding: 12px 15px;
            background: transparent;
            font-size: 14px;
            border-radius: 20px;
        }

        .send-button {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #ff6b6b, #feca57);
            border: none;
            border-radius: 50%;
            color: white;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
        }

        .send-button:hover {
            transform: scale(1.1);
            box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
        }

        .quick-replies {
            display: flex;
            gap: 8px;
            margin-bottom: 10px;
            flex-wrap: wrap;
        }

        .quick-reply {
            background: linear-gradient(135deg, #48dbfb, #0abde3);
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 15px;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .quick-reply:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(72, 219, 251, 0.4);
        }

        .message-time {
            font-size: 10px;
            opacity: 0.7;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="chatbot-container">
        <div class="chat-header">
            <div class="bot-avatar">🤖</div>
            <div class="bot-name">AI Assistant</div>
            <div class="bot-status">Online • Ready to help</div>
        </div>

        <div class="chat-messages" id="chatMessages">
            <div class="message bot-message">
                Hi there! 👋 I'm your AI assistant. How can I help you today?
                <div class="message-time">Just now</div>
            </div>
        </div>

        <div class="typing-indicator" id="typingIndicator">
            <div class="typing-dots">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        </div>

        <div class="chat-input-container">
            <div class="quick-replies">
                <button class="quick-reply" onclick="sendQuickReply('Tell me a joke')">Tell me a joke 😄</button>
                <button class="quick-reply" onclick="sendQuickReply('What can you do?')">What can you do? 🤔</button>
                <button class="quick-reply" onclick="sendQuickReply('Help me')">Help me 🆘</button>
            </div>
            <div class="input-wrapper">
                <input type="text" class="chat-input" id="chatInput" placeholder="Type your message..." onkeypress="handleKeyPress(event)">
                <button class="send-button" onclick="sendMessage()">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                    </svg>
                </button>
            </div>
        </div>
    </div>

    <script>
        const chatMessages = document.getElementById('chatMessages');
        const chatInput = document.getElementById('chatInput');
        const typingIndicator = document.getElementById('typingIndicator');

        function addMessage(message, isUser = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
            
            const now = new Date();
            const timeString = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            
            messageDiv.innerHTML = `
                ${message}
                <div class="message-time">${timeString}</div>
            `;
            
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function showTyping() {
            typingIndicator.style.display = 'block';
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function hideTyping() {
            typingIndicator.style.display = 'none';
        }

        async function getAIResponse(message) {
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });
                
                const data = await response.json();
                return data.response;
            } catch (error) {
                console.error('Error:', error);
                return 'Sorry, I encountered an error. Please try again.';
            }
        }

        async function sendMessage() {
            const message = chatInput.value.trim();
            if (message === '') return;

            addMessage(message, true);
            chatInput.value = '';

            showTyping();
            
            const aiResponse = await getAIResponse(message);
            hideTyping();
            addMessage(aiResponse);
        }

        async function sendQuickReply(message) {
            addMessage(message, true);
            
            showTyping();
            
            const aiResponse = await getAIResponse(message);
            hideTyping();
            addMessage(aiResponse);
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        // Auto-focus on input
        chatInput.focus();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '')
        
        if not user_message:
            return jsonify({'response': 'Please enter a message.'})
        
        # Get response from Meta AI
        response = ai.prompt(message=user_message)
        
        # Clean the response
        if isinstance(response, dict):
            cleaned_response = str(response.get('message', ''))
        else:
            cleaned_response = str(response).replace("\n", " ")
        
        cleaned_response = cleaned_response.replace("source:", "").replace("media:", "").strip()
        
        return jsonify({'response': cleaned_response})
    
    except Exception as e:
        return jsonify({'response': f'Sorry, I encountered an error: {str(e)}'})

def open_browser():
    """Open the browser after a short delay"""
    time.sleep(1.5)
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    print("🚀 Starting AI Chatbot...")
    print("🌐 Opening browser in a moment...")
    
    # Start browser in a separate thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run Flask app
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
