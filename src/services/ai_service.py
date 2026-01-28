import google.generativeai as genai
import os
import logging

logger = logging.getLogger(__name__)


class AIService:
    """Service for AI interactions using Google Gemini"""
    
    def __init__(self, api_key):
        """
        Initialize AI service
        
        Args:
            api_key: Google Gemini API key
        """
        if not api_key:
            raise ValueError("GEMINI_API_KEY is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        logger.info("AI Service initialized with Google Gemini")
    
    def process_message(self, user_message):
        """
        Process user message and generate AI response
        
        Args:
            user_message: User's input message
            
        Returns:
            str: AI-generated response text
            
        Raises:
            ValueError: If message is empty or invalid
            Exception: If API call fails
        """
        if not user_message or not isinstance(user_message, str):
            raise ValueError("Invalid message: must be a non-empty string")
        
        if len(user_message) > 5000:
            raise ValueError("Message too long: maximum 5000 characters")
        
        logger.info(f"Processing message (length: {len(user_message)})")
        
        try:
            system_prompt = (
                "Act like a personal assistant. You can respond to questions, "
                "translate sentences, summarize news, and give recommendations. "
                "Keep responses concise and helpful."
            )
            
            prompt = system_prompt + "\n\nUser: " + user_message
            
            response = self.model.generate_content(prompt)
            
            logger.info("AI response generated successfully")
            return response.text
            
        except Exception as e:
            logger.error(f"AI processing failed: {str(e)}")
            raise Exception(f"Failed to process message: {str(e)}")
