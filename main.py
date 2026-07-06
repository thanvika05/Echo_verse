import streamlit as st
import os
import time
from datetime import datetime
from config import Config
from api_rewriter import TextProcessor
from api_tts import AdvancedTTS
from utils.file_processor import FileProcessor
from utils.web_scraper import WebScraper
from utils.translator import LanguageTranslator

# Initialize components
Config.create_directories()
text_processor = TextProcessor()
tts = AdvancedTTS()
file_processor = FileProcessor()
web_scraper = WebScraper()
translator = LanguageTranslator()

# Page configuration
st.set_page_config(
    page_title="EchoVerse - AI Audiobook Creator",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'audio_files' not in st.session_state:
    st.session_state.audio_files = []
if 'processed_texts' not in st.session_state:
    st.session_state.processed_texts = []

# Main header
st.markdown("""
<div class="main-header">
    <h1>🎧 EchoVerse - AI Audiobook Creator</h1>
    <p>Transform any text, file, or URL into professional audiobooks with AI-powered voices</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 Quick Actions")
    
    # Input method selection
    input_method = st.radio(
        "Choose Input Method:",
        ["📝 Type Text", "📁 Upload File", "🌐 URL/Link", "🎵 Audio to Text"],
        key="input_method"
    )
    
    st.markdown("---")
    
    # Voice settings
    st.markdown("### 🎤 Voice Settings")
    language = st.selectbox("Language", list(Config.VOICES.keys()))
    gender = st.selectbox("Gender", ["Male", "Female"])
    
    # Get available voices for selected language and gender
    voices = tts.get_available_voices(language, gender)
    if voices:
        voice_options = [f"{v['display_name']}" for v in voices]
        selected_voice = st.selectbox("Voice", voice_options)
        selected_voice_id = voices[voice_options.index(selected_voice)]['voice_id']
    else:
        selected_voice_id = "en-US-JennyNeural"
    
    # Audio settings
    st.markdown("### ⚙️ Audio Settings")
    speech_rate = st.slider("Speech Rate", -50, 50, 0, help="Speed of speech (-50 to +50)")
    volume = st.slider("Volume", -50, 50, 0, help="Volume level (-50 to +50)")
    
    st.markdown("---")
    
    # History
    if st.session_state.audio_files:
        st.markdown("### 📚 Recent Audio Files")
        for i, audio_file in enumerate(st.session_state.audio_files[-5:]):
            st.write(f"🎵 {os.path.basename(audio_file)}")

# Main content area
tab1, tab2, tab3, tab4 = st.tabs(["🎧 Create Audiobook", "🌐 URL Processing", "🔄 Audio to Text", "📊 History & Downloads"])

with tab1:
    st.markdown("### 🎧 Create Your Audiobook")
    
    # Input processing based on selected method
    input_text = ""
    
    if input_method == "📝 Type Text":
        input_text = st.text_area("Enter your text here:", height=200, placeholder="Type or paste your text here...")
        
    elif input_method == "📁 Upload File":
        uploaded_file = st.file_uploader(
            "Upload a file (PDF, DOCX, TXT)",
            type=['pdf', 'docx', 'txt'],
            help="Supported formats: PDF, DOCX, TXT"
        )
        
        if uploaded_file:
            # Save uploaded file
            file_path = os.path.join(Config.UPLOAD_FOLDER, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            try:
                # Process file
                with st.spinner("Processing file..."):
                    file_data = file_processor.process_file(file_path)
                    input_text = file_data['text']
                
                # Display file info
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Words", file_data['word_count'])
                with col2:
                    st.metric("Characters", file_data['char_count'])
                with col3:
                    st.metric("Reading Time", f"{file_data['estimated_reading_time']} min")
                
                st.success(f"✅ File processed successfully: {uploaded_file.name}")
                
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
    
    elif input_method == "🌐 URL/Link":
        url_input = st.text_input("Enter URL:", placeholder="https://example.com/article")
        
        if url_input:
            with st.spinner("Extracting content from URL..."):
                url_data = web_scraper.extract_text_from_url(url_input)
                
                if url_data['status'] == 'success':
                    input_text = url_data['text']
                    
                    # Display URL info
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Title", url_data['title'][:30] + "..." if len(url_data['title']) > 30 else url_data['title'])
                    with col2:
                        st.metric("Words", url_data['word_count'])
                    with col3:
                        st.metric("Domain", url_data['domain'])
                    
                    st.success(f"✅ Content extracted from: {url_data['domain']}")
                else:
                    st.error(f"❌ Error extracting content: {url_data.get('error', 'Unknown error')}")
    
    elif input_method == "🎵 Audio to Text":
        audio_file = st.file_uploader(
            "Upload audio file",
            type=['mp3', 'wav', 'm4a'],
            help="Upload audio file to convert to text"
        )
        
        if audio_file:
            # Save audio file
            audio_path = os.path.join(Config.UPLOAD_FOLDER, audio_file.name)
            with open(audio_path, "wb") as f:
                f.write(audio_file.getbuffer())
            
            # Process audio to text (simplified - would need speech recognition library)
            st.info("🎵 Audio to text conversion feature requires additional speech recognition libraries. For now, please use text input.")
    
    # Text processing options
    if input_text:
        st.markdown("### 📝 Text Processing Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            process_text = st.checkbox("🔄 Process & Enhance Text", value=True)
            if process_text:
                style = st.selectbox("Text Style", ["natural", "formal", "casual"])
                tone = st.selectbox("Tone", ["neutral", "positive", "professional"])
        
        with col2:
            translate_text = st.checkbox("🌍 Translate Text")
            if translate_text:
                target_language = st.selectbox("Target Language", translator.get_supported_languages())
                create_multilingual = st.checkbox("Create multilingual audio")
        
        # Process text
        processed_text = input_text
        if process_text:
            with st.spinner("Processing text..."):
                processed_text = text_processor.rewrite_text(input_text, style, tone)
        
        # Translate if requested
        if translate_text:
            with st.spinner("Translating text..."):
                translation = translator.translate_text(processed_text, target_language)
                if translation['status'] == 'success':
                    processed_text = translation['translated_text']
                    st.success(f"✅ Translated to {target_language}")
                else:
                    st.error(f"❌ Translation failed: {translation.get('error', 'Unknown error')}")
        
        # Display processed text
        if processed_text != input_text:
            with st.expander("📝 View Processed Text"):
                st.text_area("Processed Text", processed_text, height=200)
        
        # Generate audio
        if st.button("🎧 Generate Audiobook", type="primary"):
            if processed_text:
                with st.spinner("Generating audio..."):
                    try:
                        # Create filename
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"echoverse_audio_{timestamp}.mp3"
                        
                        # Generate audio
                        audio_path = tts.text_to_speech(
                            text=processed_text,
                            filename=filename,
                            voice=selected_voice_id,
                            language=language,
                            rate=f"{speech_rate:+d}%",
                            volume=f"{volume:+d}%"
                        )
                        
                        # Add to session state
                        st.session_state.audio_files.append(audio_path)
                        st.session_state.processed_texts.append({
                            'text': processed_text,
                            'language': language,
                            'voice': selected_voice_id,
                            'timestamp': timestamp
                        })
                        
                        st.success("✅ Audiobook generated successfully!")
                        
                        # Display audio player
                        st.audio(audio_path)
                        
                        # Download button
                        with open(audio_path, "rb") as audio_file:
                            st.download_button(
                                label="📥 Download Audio",
                                data=audio_file.read(),
                                file_name=filename,
                                mime="audio/mpeg"
                            )
                        
                        # Audio info
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("File Size", f"{os.path.getsize(audio_path) / (1024*1024):.1f} MB")
                        with col2:
                            st.metric("Language", language)
                        with col3:
                            st.metric("Voice", f"{gender} - {selected_voice_id.split('-')[-1]}")
                        
                    except Exception as e:
                        st.error(f"❌ Error generating audio: {str(e)}")
            else:
                st.warning("⚠️ Please enter some text to generate audio.")

with tab2:
    st.markdown("### 🌐 URL Content Processing")
    
    url_input = st.text_input("Enter URL to process:", placeholder="https://example.com/article")
    
    if url_input:
        if st.button("🔍 Extract & Process"):
            with st.spinner("Processing URL..."):
                url_data = web_scraper.extract_text_from_url(url_input)
                
                if url_data['status'] == 'success':
                    st.success(f"✅ Content extracted from: {url_data['domain']}")
                    
                    # Display content info
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Title", url_data['title'][:30] + "..." if len(url_data['title']) > 30 else url_data['title'])
                    with col2:
                        st.metric("Words", url_data['word_count'])
                    with col3:
                        st.metric("Characters", url_data['char_count'])
                    
                    # Show extracted content
                    with st.expander("📄 View Extracted Content"):
                        st.text_area("Content", url_data['text'], height=300)
                    
                    # Generate audio from URL content
                    if st.button("🎧 Generate Audio from URL"):
                        with st.spinner("Generating audio..."):
                            try:
                                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                filename = f"url_audio_{timestamp}.mp3"
                                
                                audio_path = tts.text_to_speech(
                                    text=url_data['text'],
                                    filename=filename,
                                    voice=selected_voice_id,
                                    language=language,
                                    rate=f"{speech_rate:+d}%",
                                    volume=f"{volume:+d}%"
                                )
                                
                                st.session_state.audio_files.append(audio_path)
                                st.success("✅ Audio generated from URL content!")
                                
                                st.audio(audio_path)
                                
                                with open(audio_path, "rb") as audio_file:
                                    st.download_button(
                                        label="📥 Download Audio",
                                        data=audio_file.read(),
                                        file_name=filename,
                                        mime="audio/mpeg"
                                    )
                                    
                            except Exception as e:
                                st.error(f"❌ Error generating audio: {str(e)}")
                else:
                    st.error(f"❌ Error extracting content: {url_data.get('error', 'Unknown error')}")

with tab3:
    st.markdown("### 🔄 Audio to Text Conversion")
    st.info("🎵 This feature requires additional speech recognition libraries. For now, please use the text input method.")
    
    # Placeholder for future audio-to-text functionality
    st.markdown("""
    **Planned Features:**
    - Upload audio files (MP3, WAV, M4A)
    - Convert speech to text
    - Support multiple languages
    - Gender detection from audio
    - Text editing and correction
    """)

with tab4:
    st.markdown("### 📊 History & Downloads")
    
    if st.session_state.audio_files:
        st.markdown("#### 🎵 Generated Audio Files")
        
        for i, audio_file in enumerate(st.session_state.audio_files):
            if os.path.exists(audio_file):
                with st.expander(f"🎧 {os.path.basename(audio_file)}"):
                    st.audio(audio_file)
                    
                    # File info
                    file_size = os.path.getsize(audio_file) / (1024 * 1024)
                    st.write(f"📁 File Size: {file_size:.1f} MB")
                    
                    # Download button
                    with open(audio_file, "rb") as f:
                        st.download_button(
                            label="📥 Download",
                            data=f.read(),
                            file_name=os.path.basename(audio_file),
                            mime="audio/mpeg",
                            key=f"download_{i}"
                        )
                    
                    # Delete button
                    if st.button(f"🗑️ Delete", key=f"delete_{i}"):
                        try:
                            os.remove(audio_file)
                            st.session_state.audio_files.pop(i)
                            st.success("✅ File deleted successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error deleting file: {str(e)}")
    else:
        st.info("📭 No audio files generated yet. Create your first audiobook in the 'Create Audiobook' tab!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🎧 EchoVerse - AI-Powered Audiobook Creation Tool</p>
    <p>Transform any content into professional audiobooks with ease</p>
</div>
""", unsafe_allow_html=True)
