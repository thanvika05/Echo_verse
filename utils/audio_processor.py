import speech_recognition as sr
import librosa
import numpy as np
from pydub import AudioSegment
import os
import tempfile
from typing import Dict, Any, Optional
import soundfile as sf
from config import Config

class AudioProcessor:
    """Handles audio processing, speech-to-text conversion, and audio analysis"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
    
    def speech_to_text(self, audio_file_path: str, language: str = 'en-US') -> Dict[str, Any]:
        """Convert speech to text from audio file"""
        try:
            # Load audio file
            with sr.AudioFile(audio_file_path) as source:
                audio = self.recognizer.record(source)
            
            # Perform speech recognition
            text = self.recognizer.recognize_google(audio, language=language)
            
            return {
                'text': text,
                'confidence': 0.8,  # Google doesn't provide confidence
                'language': language,
                'status': 'success',
                'word_count': len(text.split()),
                'char_count': len(text)
            }
            
        except sr.UnknownValueError:
            return {
                'error': 'Speech could not be understood',
                'status': 'error'
            }
        except sr.RequestError as e:
            return {
                'error': f'Could not request results: {str(e)}',
                'status': 'error'
            }
        except Exception as e:
            return {
                'error': f'Error processing audio: {str(e)}',
                'status': 'error'
            }
    
    def detect_gender_from_audio(self, audio_file_path: str) -> Dict[str, Any]:
        """Detect gender from audio using pitch analysis"""
        try:
            # Load audio file
            y, sr = librosa.load(audio_file_path)
            
            # Extract pitch features
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
            
            # Get the pitch values where magnitude is above threshold
            pitch_values = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    pitch_values.append(pitch)
            
            if not pitch_values:
                return {
                    'gender': 'unknown',
                    'confidence': 0.0,
                    'average_pitch': 0,
                    'status': 'error'
                }
            
            # Calculate average pitch
            avg_pitch = np.mean(pitch_values)
            
            # Gender classification based on pitch
            # Male voices typically have lower pitch (85-180 Hz)
            # Female voices typically have higher pitch (165-255 Hz)
            if avg_pitch < 150:
                gender = 'male'
                confidence = min(1.0, (150 - avg_pitch) / 50)
            elif avg_pitch > 200:
                gender = 'female'
                confidence = min(1.0, (avg_pitch - 200) / 50)
            else:
                # Ambiguous range
                if avg_pitch < 175:
                    gender = 'male'
                    confidence = 0.6
                else:
                    gender = 'female'
                    confidence = 0.6
            
            return {
                'gender': gender,
                'confidence': confidence,
                'average_pitch': avg_pitch,
                'pitch_range': (min(pitch_values), max(pitch_values)),
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'error': f'Error detecting gender: {str(e)}',
                'status': 'error'
            }
    
    def analyze_audio(self, audio_file_path: str) -> Dict[str, Any]:
        """Comprehensive audio analysis"""
        try:
            # Load audio
            y, sr = librosa.load(audio_file_path)
            
            # Basic audio properties
            duration = librosa.get_duration(y=y, sr=sr)
            
            # Spectral features
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
            
            # MFCC features
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            
            # Tempo
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            
            # Zero crossing rate
            zcr = librosa.feature.zero_crossing_rate(y)[0]
            
            return {
                'duration': duration,
                'sample_rate': sr,
                'tempo': tempo,
                'average_spectral_centroid': np.mean(spectral_centroids),
                'average_spectral_rolloff': np.mean(spectral_rolloff),
                'average_zero_crossing_rate': np.mean(zcr),
                'mfcc_mean': np.mean(mfccs, axis=1).tolist(),
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'error': f'Error analyzing audio: {str(e)}',
                'status': 'error'
            }
    
    def convert_audio_format(self, input_path: str, output_path: str, format: str = 'mp3') -> bool:
        """Convert audio file to different format"""
        try:
            audio = AudioSegment.from_file(input_path)
            audio.export(output_path, format=format)
            return True
        except Exception as e:
            print(f"Error converting audio: {str(e)}")
            return False
    
    def extract_audio_from_video(self, video_path: str, output_path: str) -> bool:
        """Extract audio from video file"""
        try:
            video = AudioSegment.from_file(video_path)
            audio = video.set_channels(1).set_frame_rate(22050)
            audio.export(output_path, format="wav")
            return True
        except Exception as e:
            print(f"Error extracting audio from video: {str(e)}")
            return False
    
    def split_audio_by_silence(self, audio_file_path: str, min_silence_len: int = 1000, silence_thresh: int = -40) -> list:
        """Split audio file by silence detection"""
        try:
            audio = AudioSegment.from_file(audio_file_path)
            
            # Split audio by silence
            chunks = split_on_silence(
                audio,
                min_silence_len=min_silence_len,
                silence_thresh=silence_thresh,
                keep_silence=500
            )
            
            # Save chunks
            chunk_paths = []
            for i, chunk in enumerate(chunks):
                chunk_path = f"temp/chunk_{i}.wav"
                chunk.export(chunk_path, format="wav")
                chunk_paths.append(chunk_path)
            
            return chunk_paths
            
        except Exception as e:
            print(f"Error splitting audio: {str(e)}")
            return []
    
    def enhance_audio_quality(self, input_path: str, output_path: str) -> bool:
        """Enhance audio quality using basic filters"""
        try:
            audio = AudioSegment.from_file(input_path)
            
            # Apply basic enhancements
            # Normalize volume
            audio = audio.normalize()
            
            # Apply high-pass filter to remove low-frequency noise
            audio = audio.high_pass_filter(80)
            
            # Apply low-pass filter to remove high-frequency noise
            audio = audio.low_pass_filter(8000)
            
            # Export enhanced audio
            audio.export(output_path, format="mp3")
            return True
            
        except Exception as e:
            print(f"Error enhancing audio: {str(e)}")
            return False
    
    def detect_language_from_audio(self, audio_file_path: str) -> Dict[str, Any]:
        """Attempt to detect language from audio using speech recognition"""
        # List of languages to try
        languages = ['en-US', 'es-ES', 'fr-FR', 'de-DE', 'hi-IN', 'zh-CN']
        
        best_result = None
        best_confidence = 0
        
        for lang in languages:
            result = self.speech_to_text(audio_file_path, lang)
            if result['status'] == 'success':
                # Simple heuristic: longer text usually means better recognition
                confidence = len(result['text']) / 100  # Normalize by expected length
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_result = result
                    best_result['detected_language'] = lang
        
        if best_result:
            return best_result
        else:
            return {
                'error': 'Could not detect language from audio',
                'status': 'error'
            }

# Helper function for silence detection
def split_on_silence(audio_segment, min_silence_len=1000, silence_thresh=-40, keep_silence=500):
    """Split audio segment on silence"""
    from pydub.silence import split_on_silence
    return split_on_silence(audio_segment, min_silence_len, silence_thresh, keep_silence)
