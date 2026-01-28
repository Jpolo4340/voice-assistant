from flask import Flask
from flask_cors import CORS
import logging

from src.config import get_config
from src.utils.logger import setup_logger
from src.services.ai_service import AIService
from src.services.speech_service import SpeechRecognitionService
from src.services.tts_service import TextToSpeechService
from src.routes.main import main_bp
from src.routes.api import api_bp, init_services


def create_app():
    """
    Create and configure the Flask application
    
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    # Load configuration
    config = get_config()
    app.config.from_object(config)
    
    # Setup logging
    log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
    setup_logger('voice_assistant', config.LOG_FILE, log_level)
    logger = logging.getLogger('voice_assistant')
    
    logger.info(f"Starting Voice Assistant in {config.FLASK_ENV} mode")
    
    # Enable CORS for all routes
    CORS(app)
    
    # Initialize services
    try:
        ai_service = AIService(config.GEMINI_API_KEY)
        speech_service = SpeechRecognitionService()
        tts_service = TextToSpeechService()
        
        # Pass services to API routes
        init_services(speech_service, ai_service, tts_service)
        
        logger.info("All services initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        raise
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    
    logger.info("Application configured successfully")
    
    return app


def main():
    """Main entry point for the application"""
    app = create_app()
    config = get_config()
    
    logger = logging.getLogger('voice_assistant')
    logger.info(f"Starting server on {config.HOST}:{config.PORT}")
    
    app.run(
        debug=config.FLASK_DEBUG,
        host=config.HOST,
        port=config.PORT
    )


if __name__ == '__main__':
    main()
