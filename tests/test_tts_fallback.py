"""
Test for text-to-speech service
"""
from src.services.tts_service import TextToSpeechService
import time


def test_tts_service():
    """Test TTS service initialization and basic functionality"""
    print("Testing text-to-speech service...")
    
    # Initialize service
    tts_service = TextToSpeechService()
    
    # Test with simple text
    start = time.time()
    try:
        result = tts_service.text_to_speech("Hello testing", voice="default")
        end = time.time()
        
        print(f"Time taken: {end - start:.2f}s")
        
        if result and isinstance(result, bytes) and len(result) > 0:
            print(f"SUCCESS: Generated audio data ({len(result)} bytes)")
            return True
        else:
            print("FAILED: No audio data generated")
            return False
            
    except Exception as e:
        end = time.time()
        print(f"Time taken: {end - start:.2f}s")
        print(f"ERROR: {str(e)}")
        return False


if __name__ == "__main__":
    success = test_tts_service()
    exit(0 if success else 1)
