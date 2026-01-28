# Voice Assistant with Google Gemini

A production-ready voice assistant application powered by Google Gemini AI, Google Speech Recognition, and Microsoft Edge Text-to-Speech. Users can interact via text or voice input and receive intelligent spoken responses.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini-orange.svg)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-PEP8-black)](https://www.python.org/dev/peps/pep-0008/)

## Features

- **Voice Input** - Speak your questions using your microphone
- **Text Input** - Type messages for quick interactions
- **Voice Output** - Get spoken responses from the assistant
- **Dark/Light Theme** - Toggle between themes for comfort
- **Multiple Voices** - Choose from various voice options
- **AI-Powered** - Leverages Google Gemini for intelligent responses
- **Responsive Design** - Works on desktop and mobile devices
- **Production-Ready** - Proper logging, error handling, and configuration management

## Technology Stack

### Backend

- **Python 3.8+**
- **Flask 3.0.0** - Web framework
- **Google Gemini API** - AI processing and natural language understanding
- **Google Speech Recognition** - Speech-to-text conversion
- **Microsoft Edge TTS** - Text-to-speech synthesis
- **Gunicorn** - Production WSGI server

### Frontend

- **HTML5** - Semantic markup
- **CSS3** - Modern styling with custom properties
- **JavaScript** - Interactive features and API communication
- **Bootstrap 5** - UI framework
- **Font Awesome** - Icons

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A Google Gemini API key - [Get one here](https://aistudio.google.com/apikey)
- A modern web browser with microphone support

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/hasancoded/voice-assistant.git
cd voice-assistant
```

2. **Create and activate virtual environment**

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

> **Note:** On some systems, you may need to install additional dependencies for PyAudio:
>
> - **Ubuntu/Debian:** `sudo apt-get install portaudio19-dev python3-pyaudio`
> - **macOS:** `brew install portaudio`
> - **Windows:** PyAudio binaries are available via pip

4. **Configure environment variables**

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your Google Gemini API key
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

5. **Run the application**

```bash
python -m src.app
```

The application will start on <http://localhost:8080>

6. **Open in browser**

Navigate to <http://localhost:8080> and allow microphone access when prompted.

## Docker Deployment

```bash
# Build the Docker image
docker build -t voice-assistant .

# Run the container
docker run -p 8080:8080 -e GEMINI_API_KEY=your_key voice-assistant
```

## Project Structure

```
voice-assistant/
├── src/
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration management
│   ├── routes/
│   │   ├── main.py         # Main page and health check routes
│   │   └── api.py          # API endpoints
│   ├── services/
│   │   ├── ai_service.py   # Google Gemini integration
│   │   ├── speech_service.py # Speech-to-text service
│   │   └── tts_service.py  # Text-to-speech service
│   └── utils/
│       └── logger.py       # Logging configuration
├── templates/
│   └── index.html          # Main HTML page
├── static/
│   ├── css/
│   │   └── style.css       # Styling
│   └── js/
│       └── script.js       # Frontend JavaScript
├── tests/                  # Test files
├── scripts/                # Utility scripts
├── logs/                   # Application logs
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── LICENSE                # MIT License
└── README.md              # This file
```

## Usage

### Text Input

1. Type your message in the input box
2. Press Enter or click the send button
3. Wait for the AI response

### Voice Input

1. Click the microphone button
2. Speak your question clearly
3. Click the stop button (or wait)
4. The assistant will transcribe and respond

### Changing Voice

Use the dropdown menu in the header to select different voice options:

- Default (US Female)
- Emily (US Female)
- Michael (US Male)
- James (UK Male)
- Allison (US Female)

### Theme Toggle

Click the moon/sun icon in the header to switch between light and dark themes.

## API Endpoints

### `GET /`

Serves the main application page.

### `GET /health`

Health check endpoint for monitoring.

**Response:**

```json
{
  "status": "healthy",
  "service": "voice-assistant"
}
```

### `POST /speech-to-text`

Convert speech audio to text.

**Request:** Binary audio data (WAV format)

**Response:**

```json
{
  "text": "transcribed text"
}
```

### `POST /process-message`

Process user message and generate AI response with speech.

**Request:**

```json
{
  "userMessage": "your message here",
  "voice": "en-US_EmilyV3Voice"
}
```

**Response:**

```json
{
  "openaiResponseText": "AI response text",
  "openaiResponseSpeech": "base64_encoded_audio"
}
```

## Configuration

All configuration can be managed through environment variables in `.env`:

```bash
# AI Service Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Server Configuration
FLASK_ENV=production
FLASK_DEBUG=False
PORT=8080
HOST=0.0.0.0

# Logging
LOG_LEVEL=INFO
```

## Troubleshooting

### Module not found errors

Ensure virtual environment is activated and dependencies are installed:

```bash
pip install -r requirements.txt
```

### Microphone not working

- Check browser permissions (click the lock icon in address bar)
- Use HTTPS or localhost (required for microphone access)
- Try a different browser (Chrome/Edge recommended)

### Google Gemini API errors

- Verify your API key in `.env` is correct
- Check you have API access enabled in Google AI Studio
- Ensure you're using a valid model name

### Port already in use

Change the port in `.env`:

```bash
PORT=8081
```

## Security Notes

- **Never commit your `.env` file** - It contains sensitive API keys
- Keep your Google Gemini API key secure
- Use environment variables for all secrets
- Be mindful of API usage costs
- Implement rate limiting for production use

## API Costs

Be aware of API usage costs:

- **Google Gemini** - Free tier available, check current pricing at <https://ai.google.dev/pricing>
- **Google Speech Recognition** - Free tier available for limited usage
- **Microsoft Edge TTS** - Free service

Monitor your usage in the Google AI Studio dashboard.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Resources

- [Google Gemini Documentation](https://ai.google.dev/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [Microsoft Edge TTS](https://github.com/rany2/edge-tts)

## Support

If you encounter any issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review the logs in `logs/app.log`
3. Check the browser console for JavaScript errors (F12)
4. Open an issue on GitHub

---

**Professional voice assistant powered by Google Gemini AI**
