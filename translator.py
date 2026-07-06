from googletrans import Translator
from typing import Dict, Any, List

class LanguageTranslator:
    """Handles text translation between multiple languages"""
    
    def __init__(self):
        self.translator = Translator()
        
        # Supported languages mapping
        self.language_map = {
            'English': 'en',
            'Spanish': 'es',
            'French': 'fr',
            'German': 'de',
            'Hindi': 'hi',
            'Chinese': 'zh-cn',
            'Japanese': 'ja',
            'Korean': 'ko',
            'Italian': 'it',
            'Portuguese': 'pt',
            'Russian': 'ru',
            'Arabic': 'ar'
        }
        
        # Reverse mapping for display
        self.reverse_language_map = {v: k for k, v in self.language_map.items()}
    
    def translate_text(self, text: str, target_language: str, source_language: str = 'auto') -> Dict[str, Any]:
        """Translate text to target language"""
        try:
            # Convert language names to codes
            target_code = self.language_map.get(target_language, target_language)
            source_code = self.language_map.get(source_language, source_language) if source_language != 'auto' else 'auto'
            
            # Perform translation
            result = self.translator.translate(
                text, 
                dest=target_code, 
                src=source_code
            )
            
            return {
                'original_text': text,
                'translated_text': result.text,
                'source_language': self.reverse_language_map.get(result.src, result.src),
                'target_language': target_language,
                'confidence': 0.9,  # Google Translate doesn't provide confidence
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'error': f'Translation failed: {str(e)}',
                'status': 'error'
            }
    
    def detect_language(self, text: str) -> Dict[str, Any]:
        """Detect the language of the input text"""
        try:
            result = self.translator.detect(text)
            
            return {
                'text': text,
                'detected_language': self.reverse_language_map.get(result.lang, result.lang),
                'language_code': result.lang,
                'confidence': result.confidence,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'error': f'Language detection failed: {str(e)}',
                'status': 'error'
            }
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        return list(self.language_map.keys())
