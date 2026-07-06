import os

class Config:
    # File paths
    UPLOAD_FOLDER = 'uploads'
    AUDIO_FOLDER = 'audio_outputs'
    TEMP_FOLDER = 'temp'
    
    # Supported file types
    SUPPORTED_TEXT_FILES = ['.txt', '.pdf', '.docx']
    SUPPORTED_AUDIO_FILES = ['.mp3', '.wav', '.m4a']
    
    # Voice options
    VOICES = {
        'English': {
            'Male': ['en-US-GuyNeural', 'en-AU-WilliamNeural'],
            'Female': ['en-US-JennyNeural', 'en-US-AriaNeural']
        },
        'Spanish': {
            'Male': ['es-ES-AlvaroNeural'],
            'Female': ['es-ES-ElviraNeural']
        },
        'French': {
            'Male': ['fr-FR-HenriNeural'],
            'Female': ['fr-FR-DeniseNeural']
        },
        'German': {
            'Male': ['de-DE-ConradNeural'],
            'Female': ['de-DE-KatjaNeural']
        }
    }
    
    # Audio settings
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    
    # Web scraping settings
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    
    # Create necessary directories
    @staticmethod
    def create_directories():
        for folder in [Config.UPLOAD_FOLDER, Config.AUDIO_FOLDER, Config.TEMP_FOLDER]:
            os.makedirs(folder, exist_ok=True)
