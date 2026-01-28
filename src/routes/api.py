from flask import Blueprint, request, jsonify
import json
import base64
import os
import logging

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)

# Services will be initialized in app.py and set here
speech_service = None
ai_service = None
tts_service = None


def init_services(speech_svc, ai_svc, tts_svc):
    """Initialize services for API routes"""
    global speech_service, ai_service, tts_service
    speech_service = speech_svc
    ai_service = ai_svc
    tts_service = tts_svc


@api_bp.route('/speech-to-text', methods=['POST'])
def speech_to_text_route():
    """
    Handle speech-to-text conversion
    
    Expects:
        Binary audio data in request body
        
    Returns:
        JSON: {'text': transcribed_text} or error response
    """
    logger.info("Processing speech-to-text request")
    
    try:
        # Get the user's audio from request
        audio_binary = request.data
        
        if not audio_binary:
            logger.warning("No audio data received")
            return jsonify({'error': 'No audio data provided'}), 400
        
        # Call speech_to_text function to transcribe the speech
        text = speech_service.speech_to_text(audio_binary)
        
        logger.info(f"Transcription successful: {text}")
        return jsonify({'text': text}), 200
        
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        return jsonify({'error': str(e)}), 400
        
    except Exception as e:
        logger.error(f"Speech-to-text failed: {str(e)}")
        return jsonify({'error': 'Failed to process audio'}), 500


@api_bp.route('/process-message', methods=['POST'])
def process_message_route():
    """
    Process user message through AI and convert response to speech
    
    Expects:
        JSON: {
            'userMessage': str,
            'voice': str (optional)
        }
        
    Returns:
        JSON: {
            'openaiResponseText': str,
            'openaiResponseSpeech': str (base64 encoded audio)
        }
    """
    logger.info("Processing message request")
    
    try:
        # Validate request has JSON body
        if not request.json:
            logger.warning("No JSON body in request")
            return jsonify({'error': 'No JSON body provided'}), 400
        
        # Get user's message from request
        user_message = request.json.get('userMessage')
        if not user_message:
            logger.warning("No userMessage in request")
            return jsonify({'error': 'userMessage is required'}), 400
        
        # Get user's preferred voice
        voice = request.json.get('voice', '')
        
        logger.info(f"User message: {user_message[:50]}... | Voice: {voice}")
        
        # Process message with AI
        ai_response_text = ai_service.process_message(user_message)
        
        # Clean the response to remove any empty lines
        ai_response_text = os.linesep.join([
            s for s in ai_response_text.splitlines() if s
        ])
        
        # Convert AI response to speech
        ai_response_speech = tts_service.text_to_speech(ai_response_text, voice)
        
        # Convert audio to base64 string for JSON response
        ai_response_speech_b64 = base64.b64encode(ai_response_speech).decode('utf-8')
        
        logger.info("Message processed successfully")
        
        # Send JSON response back
        return jsonify({
            "openaiResponseText": ai_response_text,
            "openaiResponseSpeech": ai_response_speech_b64
        }), 200
        
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        return jsonify({'error': str(e)}), 400
        
    except Exception as e:
        logger.error(f"Message processing failed: {str(e)}")
        return jsonify({'error': 'Failed to process message'}), 500
