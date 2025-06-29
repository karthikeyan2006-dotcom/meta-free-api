# KARTHIKEYAN'S META AI CHATBOT

A modern web interface for Meta AI chatbot with real-time conversation capabilities.

## Features

- 🤖 **Meta AI Integration**: Direct integration with Meta AI API
- 💬 **Real-time Chat**: Instant responses with typing indicators
- 🎨 **Modern UI**: Beautiful gradient design with animations
- 📱 **Responsive**: Works on desktop and mobile devices
- 🔄 **Connection Status**: Real-time server connection monitoring
- ⚡ **Quick Replies**: Pre-defined conversation starters
- 📝 **Message History**: Conversation history management

## Prerequisites

Before running the application, make sure you have:

1. **Node.js** (version 14 or higher)
2. **Python 3** with the Meta AI API package:
   ```bash
   pip install meta_ai_api
   ```

## Installation

1. **Clone or download the project files**

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Verify Python Meta AI installation**:
   ```bash
   python3 -c "from meta_ai_api import MetaAI; print('Meta AI API is ready!')"
   ```

## Usage

### Method 1: Using the Web Interface (Recommended)

1. **Start the server**:
   ```bash
   npm start
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:3000
   ```

3. **Start chatting** with the Meta AI assistant!

### Method 2: Using Python directly

1. **Run the original Python script**:
   ```bash
   python3 metaaiapi.py
   ```

2. **Or use the Flask web version**:
   ```bash
   python3 integratedaiweb.py
   ```

### Method 3: Using the integration script

```bash
python3 meta_ai_integration.py "Hello, how are you?"
```

## API Endpoints

The Node.js server provides the following endpoints:

- `GET /` - Main chat interface
- `POST /api/chat` - Send message to Meta AI
- `GET /api/history` - Get conversation history
- `DELETE /api/history` - Clear conversation history
- `GET /api/health` - Server health check

## File Structure

```
├── package.json              # Node.js dependencies
├── server.js                 # Express server with Meta AI integration
├── public/
│   └── index.html            # Modern chat interface
├── meta_ai_integration.py    # Python Meta AI wrapper
├── metaaiapi.py             # Original Python CLI script
├── integratedaiweb.py       # Flask web version
└── README.md                # This file
```

## Features Explained

### 🎨 Modern Design
- Gradient backgrounds with smooth animations
- Glassmorphism effects with backdrop blur
- Responsive design for all screen sizes
- Smooth message animations and transitions

### 🤖 AI Integration
- Direct communication with Meta AI API
- Error handling and connection status monitoring
- Message history and conversation context
- Real-time typing indicators

### 📱 User Experience
- Auto-focus on input field
- Enter key to send messages
- Quick reply buttons for common queries
- Scroll-to-bottom for new messages
- Connection status indicator

## Troubleshooting

### Common Issues

1. **"Meta AI API not found" error**:
   ```bash
   pip install meta_ai_api
   ```

2. **Server won't start**:
   - Make sure Node.js is installed
   - Run `npm install` to install dependencies
   - Check if port 3000 is available

3. **Python script errors**:
   - Ensure Python 3 is installed
   - Verify meta_ai_api package installation
   - Check internet connection

### Error Messages

- **"Failed to get response from AI"**: Meta AI API issue or network problem
- **"Not connected to server"**: Node.js server is not running
- **"Python script failed to execute"**: Python or package installation issue

## Customization

### Changing the Port
Edit `server.js` and modify the PORT variable:
```javascript
const PORT = process.env.PORT || 3000; // Change 3000 to your preferred port
```

### Styling
Modify the CSS in `public/index.html` to customize the appearance.

### Adding Features
- Edit `server.js` for backend functionality
- Modify `public/index.html` for frontend features

## Credits

Created by **Karthikeyan**

- Meta AI API integration
- Modern web interface design
- Real-time chat functionality

## License

MIT License - Feel free to use and modify as needed.

---

**Note**: This application requires an active internet connection to communicate with Meta AI services. Make sure you have the `meta_ai_api` Python package installed and working before running the web interface.