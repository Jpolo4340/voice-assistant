import speech_recognition as sr
import io
import logging

logger = logging.getLogger(__name__)


class SpeechRecognitionService:
    """Service for speech-to-text conversion"""
    
    def __init__(self):
        """Initialize speech recognition service"""
        self.recognizer = sr.Recognizer()
        logger.info("Speech Recognition Service initialized")
    
    def speech_to_text(self, audio_binary):
        """
        Convert speech audio to text using Google Speech Recognition
        
        Args:
            audio_binary: Binary audio data
            
        Returns:
            str: Transcribed text from the audio
            
        Raises:
            ValueError: If audio data is invalid
            Exception: If speech recognition fails
        """
        if not audio_binary:
            raise ValueError("Audio data is required")
        
        try:
            logger.info(f"Processing audio data (size: {len(audio_binary)} bytes)")
            
            # Convert binary audio to a file-like object
            audio_file = io.BytesIO(audio_binary)
            
            # Use AudioFile to read the audio data
            with sr.AudioFile(audio_file) as source:
                audio_data = self.recognizer.record(source)
            
            # Recognize speech using Google Web Speech API
            text = self.recognizer.recognize_google(audio_data)
            
            logger.info(f"Speech recognized: {text}")
            return text
            
        except sr.UnknownValueError:
            logger.warning("Speech Recognition could not understand audio")
            raise Exception("Could not understand audio")
            
        except sr.RequestError as e:
            logger.error(f"Speech Recognition service error: {e}")
            raise Exception(f"Speech Recognition service unavailable: {e}")
            
        except Exception as e:
            logger.error(f"Error in speech_to_text: {e}")
            raise Exception(f"Speech recognition failed: {e}")
