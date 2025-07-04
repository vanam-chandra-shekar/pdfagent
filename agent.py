from google import genai
import os
from dotenv import load_dotenv
import logging
from typing import Optional, Dict, List
import time


load_dotenv()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiSummarizerAgent:
    
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-1.5-flash"):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.model_name = model_name
        self.client = None
        
        if not self.api_key:
            logger.warning("No API key provided.")
            return
        
        try:
            self.client = genai.Client(api_key=self.api_key)
            logger.info(f"Gemini client initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Gemini client: {str(e)}")
            self.client = None
    
    def summarize_text(self, 
                      text: str, 
                      summary_type: str = "general",
                      focus_areas: Optional[List[str]] = None,
                      summary_length: str = "medium") -> Optional[Dict]:
        
        if not self.client:
            return {
                "error": "Gemini client not initialized. Please check your API key.",
                "success": False
            }
        
        if not text or not text.strip():
            return {
                "error": "Empty text provided for summarization",
                "success": False
            }
        
        try:
            prompt = self._build_prompt(text, summary_type, focus_areas, summary_length)
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            
            if response and hasattr(response, 'text') and response.text:
                result = {
                    "summary": response.text,
                    "provider": "google_gemini",
                    "model": self.model_name,
                    "summary_type": summary_type,
                    "summary_length": summary_length,
                    "focus_areas": focus_areas or [],
                    "timestamp": time.time(),
                    "original_text_length": len(text),
                    "summary_text_length": len(response.text),
                    "success": True
                }
                
                logger.info("Text summarization completed successfully")
                return result
            else:
                return {
                    "error": "No response received from Gemini API",
                    "success": False
                }
                
        except Exception as e:
            logger.error(f"Error during text summarization: {str(e)}")
            return {
                "error": f"Error during text summarization: {str(e)}",
                "success": False
            }
    
    def _build_prompt(self, text: str, summary_type: str, focus_areas: Optional[List[str]], summary_length: str) -> str:
        
        type_instructions = {
            "general": "Provide a comprehensive summary covering all main points and key information.",
            "bullet_points": "Create a bullet-point summary with clear, concise bullet points.",
            "executive": "Write an executive summary focusing on key decisions and strategic implications.",
            "technical": "Provide a technical summary emphasizing methodologies and technical details.",
            "academic": "Create an academic summary with main arguments and conclusions.",
            "key_insights": "Extract and summarize the key insights and takeaways.",
            "action_items": "Focus on actionable items and recommendations."
        }
        
        length_instructions = {
            "short": "Keep the summary brief (2-3 sentences or 3-5 bullet points).",
            "medium": "Provide a moderate-length summary (1-2 paragraphs or 5-8 bullet points).",
            "long": "Create a detailed summary (2-3 paragraphs or 8-12 bullet points)."
        }
        
        prompt = f"""Please analyze and summarize the following text.

**Summary Instructions:**
- {type_instructions.get(summary_type, type_instructions['general'])}
- {length_instructions.get(summary_length, length_instructions['medium'])}
"""
        
        if focus_areas:
            prompt += f"""
**Special Focus Areas:**
Pay particular attention to:
{chr(10).join(f'• {area}' for area in focus_areas)}
"""
        
        prompt += f"""
**Text to Summarize:**
{text}

**Summary:**"""
        
        return prompt
    
    def validate_api_key(self) -> bool:
        
        if not self.api_key:
            return False
        
        try:
            test_text = "This is a test document to verify API connection."
            result = self.summarize_text(test_text, summary_length="short")
            return result is not None and result.get("success", False)
        except Exception as e:
            logger.error(f"API key validation failed: {str(e)}")
            return False
    
    def get_supported_summary_types(self) -> List[str]:
        return ["general", "bullet_points", "executive", "technical", "academic", "key_insights", "action_items"]
    
    def get_supported_lengths(self) -> List[str]:
        return ["short", "medium", "long"]