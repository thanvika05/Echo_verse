import re
from typing import Dict, Any

class TextProcessor:
    """Simple text processing without complex AI models"""
    
    def __init__(self):
        pass
    
    def rewrite_text(self, text: str, style: str = "natural", tone: str = "neutral") -> str:
        """Simple text rewriting using basic text processing"""
        # Basic text cleaning and enhancement
        cleaned_text = self._clean_text(text)
        
        # Apply simple enhancements based on style and tone
        if style == "formal":
            cleaned_text = self._make_formal(cleaned_text)
        elif style == "casual":
            cleaned_text = self._make_casual(cleaned_text)
        
        if tone == "positive":
            cleaned_text = self._make_positive(cleaned_text)
        elif tone == "professional":
            cleaned_text = self._make_professional(cleaned_text)
        
        return cleaned_text
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\{\}]', '', text)
        return text.strip()
    
    def _make_formal(self, text: str) -> str:
        """Make text more formal"""
        # Simple formal language replacements
        replacements = {
            'gonna': 'going to',
            'wanna': 'want to',
            'gotta': 'got to',
            'yeah': 'yes',
            'okay': 'alright',
            'cool': 'excellent'
        }
        
        for informal, formal in replacements.items():
            text = text.replace(informal, formal)
        
        return text
    
    def _make_casual(self, text: str) -> str:
        """Make text more casual"""
        # Simple casual language replacements
        replacements = {
            'therefore': 'so',
            'furthermore': 'also',
            'moreover': 'plus',
            'consequently': 'so',
            'thus': 'so',
            'hence': 'so'
        }
        
        for formal, casual in replacements.items():
            text = text.replace(formal, casual)
        
        return text
    
    def _make_positive(self, text: str) -> str:
        """Make text more positive"""
        # Simple positive language enhancements
        text = text.replace('bad', 'challenging')
        text = text.replace('terrible', 'difficult')
        text = text.replace('awful', 'challenging')
        return text
    
    def _make_professional(self, text: str) -> str:
        """Make text more professional"""
        # Simple professional language enhancements
        text = text.replace('thing', 'element')
        text = text.replace('stuff', 'materials')
        text = text.replace('guy', 'person')
        return text
    
    def summarize_text(self, text: str, max_length: int = 200) -> str:
        """Simple text summarization"""
        sentences = text.split('. ')
        if len(sentences) <= 3:
            return text
        
        # Take first few sentences
        summary_sentences = sentences[:3]
        summary = '. '.join(summary_sentences) + '.'
        
        # Truncate if too long
        if len(summary) > max_length:
            words = summary.split()
            summary = ' '.join(words[:max_length//5]) + '...'
        
        return summary
    
    def enhance_for_audio(self, text: str, style: str = "conversational") -> str:
        """Enhance text for audio narration"""
        # Add pauses and improve flow
        text = text.replace('. ', '. \n\n')
        text = text.replace('! ', '! \n\n')
        text = text.replace('? ', '? \n\n')
        
        # Make it more conversational
        if style == "conversational":
            text = self._make_casual(text)
        
        return text
    
    def detect_text_style(self, text: str) -> Dict[str, Any]:
        """Analyze text style and characteristics"""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        
        # Calculate metrics
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        
        # Detect formality
        formal_words = ['therefore', 'furthermore', 'moreover', 'consequently', 'thus', 'hence']
        informal_words = ['gonna', 'wanna', 'gotta', 'yeah', 'okay', 'cool']
        
        formal_count = sum(1 for word in words if word.lower() in formal_words)
        informal_count = sum(1 for word in words if word.lower() in informal_words)
        
        # Determine style
        if formal_count > informal_count:
            style = "formal"
        elif informal_count > formal_count:
            style = "informal"
        else:
            style = "neutral"
        
        return {
            'style': style,
            'tone': 'neutral',
            'avg_sentence_length': round(avg_sentence_length, 2),
            'avg_word_length': round(avg_word_length, 2),
            'word_count': len(words),
            'sentence_count': len(sentences),
            'formality_score': formal_count - informal_count
        }

# Backward compatibility
def rewrite_text(text: str) -> str:
    """Legacy function for backward compatibility"""
    processor = TextProcessor()
    return processor.rewrite_text(text)
