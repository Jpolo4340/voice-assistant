import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration class"""
    
    # AI Service Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    
    # Server Configuration
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    PORT = int(os.getenv('PORT', 8080))
    HOST = os.getenv('HOST', '0.0.0.0')
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.path.join('logs', 'app.log')
    
    # API Configuration
    MAX_MESSAGE_LENGTH = 5000
    REQUEST_TIMEOUT = 30


class DevelopmentConfig(Config):
    """Development environment configuration"""
    FLASK_DEBUG = True
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    """Production environment configuration"""
    FLASK_DEBUG = False
    LOG_LEVEL = 'INFO'


def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'production')
    
    if env == 'development':
        return DevelopmentConfig()
    return ProductionConfig()
