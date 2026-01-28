import edge_tts
import asyncio
import logging

logger = logging.getLogger(__name__)


# Voice Mapping (Frontend ID to Edge TTS Voice)
VOICE_MAPPING = {
    'default': 'en-US-AriaNeural',
    'en-US_EmilyV3Voice': 'en-US-AriaNeural',
    'en-US_MichaelV3Voice': 'en-US-GuyNeural',
    'en-GB_JamesV3Voice': 'en-GB-RyanNeural',
    'en-US_AllisonV3Voice': 'en-US-JennyNeural'
}


class TextToSpeechService:
    """Service for text-to-speech conversion using Microsoft Edge TTS"""
    
    def __init__(self):
        """Initialize text-to-speech service"""
        logger.info("Text-to-Speech Service initialized")
    
    def text_to_speech(self, text, voice=""):
        """
        Convert text to speech using Microsoft Edge TTS
        
        Args:
            text: Text to convert to speech
            voice: Voice ID from frontend (optional)
            
        Returns:
            bytes: Audio data in MP3 format
            
        Raises:
            ValueError: If text is invalid
            Exception: If TTS conversion fails
        """
        if not text or not isinstance(text, str):
            raise ValueError("Text must be a non-empty string")
        
        if len(text) > 5000:
            raise ValueError("Text too long: maximum 5000 characters")
        
        try:
            # Determine voice
            selected_voice = VOICE_MAPPING.get(voice, 'en-US-AriaNeural')
            logger.info(f"Generating audio with voice: {selected_voice} (requested: {voice})")
            
            async def generate_audio():
                communicate = edge_tts.Communicate(text, selected_voice)
                audio_data = b""
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        audio_data += chunk["data"]
                return audio_data
            
            # Run async function in sync context
            audio_bytes = asyncio.run(generate_audio())
            
            logger.info(f"Generated audio data (size: {len(audio_bytes)} bytes)")
            return audio_bytes
            
        except Exception as e:
            logger.error(f"Error in text_to_speech: {e}")
            raise Exception(f"Text-to-speech conversion failed: {e}")
