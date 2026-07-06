import edge_tts
import asyncio
import os
import time
from typing import Dict, Any, List
from config import Config

class AdvancedTTS:
    """Advanced Text-to-Speech with multiple providers and features"""
    
    def __init__(self):
        self.voice_map = Config.VOICES
        
    async def generate_tts(self, text: str, voice: str, audio_path: str, rate: str = "+0%", volume: str = "+0%"):
        """Generate TTS using Edge TTS"""
        try:
            communicate = edge_tts.Communicate(
                text=text, 
                voice=voice,
                rate=rate,
                volume=volume
            )
            audio_buffer = bytearray()

            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_buffer.extend(chunk["data"])

            with open(audio_path, "wb") as audio_file:
                audio_file.write(audio_buffer)
                
            return True
        except Exception as e:
            print(f"TTS generation error: {str(e)}")
            return False

    def text_to_speech(self, text: str, filename: str = "output.mp3", voice: str = "en-US-JennyNeural", 
                      language: str = "English", rate: str = "+0%", volume: str = "+0%") -> str:
        """Generate speech from text with advanced options"""
        
        # Create output directory
        os.makedirs(Config.AUDIO_FOLDER, exist_ok=True)
        audio_path = os.path.join(Config.AUDIO_FOLDER, filename)

        # Remove existing file if it exists
        if os.path.exists(audio_path):
            os.remove(audio_path)

        start = time.time()
        
        # Generate TTS
        success = asyncio.run(self.generate_tts(text, voice, audio_path, rate, volume))
        
        if success:
            print(f"⏱️ TTS Generation took {time.time() - start:.2f} seconds")
            return audio_path
        else:
            raise Exception("Failed to generate TTS audio")

    def get_available_voices(self, language: str = None, gender: str = None) -> List[Dict[str, str]]:
        """Get available voices filtered by language and gender"""
        voices = []
        
        for lang, gender_voices in self.voice_map.items():
            if language and lang != language:
                continue
                
            for gen, voice_list in gender_voices.items():
                if gender and gen != gender:
                    continue
                    
                for voice_id in voice_list:
                    voices.append({
                        'voice_id': voice_id,
                        'language': lang,
                        'gender': gen,
                        'display_name': f"{lang} - {gen} - {voice_id.split('-')[-1]}"
                    })
        
        return voices

    def create_audiobook(self, text: str, voice: str, language: str = "English", 
                        chapter_breaks: bool = True, output_filename: str = None) -> Dict[str, Any]:
        """Create a complete audiobook from text"""
        
        if not output_filename:
            output_filename = f"audiobook_{int(time.time())}.mp3"
        
        # Split text into manageable chunks
        chunks = self._split_text_for_audio(text, chapter_breaks)
        
        audio_segments = []
        total_duration = 0
        
        for i, chunk in enumerate(chunks):
            if chunk.strip():
                # Generate audio for each chunk
                chunk_filename = f"chunk_{i}_{output_filename}"
                chunk_path = self.text_to_speech(
                    chunk, 
                    chunk_filename, 
                    voice, 
                    language
                )
                
                # Load audio segment
                from pydub import AudioSegment
                segment = AudioSegment.from_mp3(chunk_path)
                audio_segments.append(segment)
                total_duration += len(segment)
                
                # Clean up chunk file
                os.remove(chunk_path)
        
        # Combine all segments
        if audio_segments:
            combined_audio = audio_segments[0]
            for segment in audio_segments[1:]:
                combined_audio += segment
            
            # Export final audiobook
            final_path = os.path.join(Config.AUDIO_FOLDER, output_filename)
            combined_audio.export(final_path, format="mp3")
            
            return {
                'file_path': final_path,
                'duration_seconds': total_duration / 1000,
                'chunks_processed': len(chunks),
                'file_size_mb': os.path.getsize(final_path) / (1024 * 1024)
            }
        else:
            raise Exception("No audio segments generated")

    def _split_text_for_audio(self, text: str, chapter_breaks: bool = True) -> List[str]:
        """Split text into audio-friendly chunks"""
        if not chapter_breaks:
            # Simple sentence-based splitting
            sentences = text.split('. ')
            chunks = []
            current_chunk = ""
            
            for sentence in sentences:
                if len(current_chunk + sentence) < 1000:  # Max 1000 characters per chunk
                    current_chunk += sentence + ". "
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = sentence + ". "
            
            if current_chunk:
                chunks.append(current_chunk.strip())
            
            return chunks
        else:
            # Chapter-based splitting
            import re
            chapter_pattern = r'(Chapter \d+|CHAPTER \d+|Chapter [A-Z]|CHAPTER [A-Z])'
            parts = re.split(f'({chapter_pattern})', text)
            
            chapters = []
            current_chapter = ""
            
            for part in parts:
                if re.match(chapter_pattern, part):
                    if current_chapter.strip():
                        chapters.append(current_chunk.strip())
                    current_chapter = part + "\n"
                else:
                    current_chapter += part
            
            if current_chapter.strip():
                chapters.append(current_chapter.strip())
            
            return chapters if chapters else [text]

    def generate_multilingual_audio(self, text: str, target_languages: List[str], 
                                  voice_gender: str = "neutral") -> Dict[str, str]:
        """Generate audio in multiple languages"""
        results = {}
        
        for language in target_languages:
            # Get appropriate voice for the language and gender
            voices = self.get_available_voices(language, voice_gender)
            if voices:
                voice_id = voices[0]['voice_id']
                
                # Translate text if needed
                from utils.translator import LanguageTranslator
                translator = LanguageTranslator()
                translation = translator.translate_text(text, language)
                
                if translation['status'] == 'success':
                    translated_text = translation['translated_text']
                else:
                    translated_text = text  # Use original text if translation fails
                
                # Generate audio
                filename = f"multilingual_{language}_{int(time.time())}.mp3"
                audio_path = self.text_to_speech(
                    translated_text,
                    filename,
                    voice_id,
                    language
                )
                
                results[language] = audio_path
        
        return results

# Backward compatibility
def text_to_speech(text, filename="output.mp3", voice="Lisa (Female)", language="English"):
    """Legacy function for backward compatibility"""
    tts = AdvancedTTS()
    voice_id = tts.voice_map.get(language, {}).get(voice.split()[1].replace('(', '').replace(')', ''), 
                                                   ['en-US-JennyNeural'])[0]
    return tts.text_to_speech(text, filename, voice_id, language)
