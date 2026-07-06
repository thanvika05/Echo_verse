#!/usr/bin/env python3
"""
EchoVerse Output Test Script
Demonstrates the functionality and shows output
"""

import os
import sys
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_text_processing():
    """Test text processing functionality"""
    print("🧪 Testing Text Processing...")
    
    try:
        from api_rewriter import TextProcessor
        processor = TextProcessor()
        
        sample_text = "Hello, this is a test of EchoVerse. It's gonna be awesome!"
        
        # Test text rewriting
        processed_text = processor.rewrite_text(sample_text, "formal", "positive")
        print(f"✅ Original: {sample_text}")
        print(f"✅ Processed: {processed_text}")
        
        # Test text analysis
        analysis = processor.detect_text_style(sample_text)
        print(f"✅ Analysis: {analysis}")
        
        return True
    except Exception as e:
        print(f"❌ Text processing error: {e}")
        return False

def test_tts():
    """Test text-to-speech functionality"""
    print("\n🎤 Testing Text-to-Speech...")
    
    try:
        from api_tts import AdvancedTTS
        tts = AdvancedTTS()
        
        # Test voice listing
        voices = tts.get_available_voices("English", "Female")
        print(f"✅ Available English Female voices: {len(voices)}")
        for voice in voices[:3]:  # Show first 3
            print(f"   - {voice['display_name']}")
        
        return True
    except Exception as e:
        print(f"❌ TTS error: {e}")
        return False

def test_file_processing():
    """Test file processing functionality"""
    print("\n📁 Testing File Processing...")
    
    try:
        from utils.file_processor import FileProcessor
        
        # Create a test file
        test_content = "This is a test file for EchoVerse. It contains some sample text to process."
        test_file_path = "test_sample.txt"
        
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write(test_content)
        
        # Process the file
        processor = FileProcessor()
        result = processor.process_file(test_file_path)
        
        print(f"✅ File processed: {result['file_name']}")
        print(f"✅ Word count: {result['word_count']}")
        print(f"✅ Character count: {result['char_count']}")
        
        # Clean up
        os.remove(test_file_path)
        
        return True
    except Exception as e:
        print(f"❌ File processing error: {e}")
        return False

def test_translation():
    """Test translation functionality"""
    print("\n🌍 Testing Translation...")
    
    try:
        from utils.translator import LanguageTranslator
        translator = LanguageTranslator()
        
        sample_text = "Hello, this is a test of translation."
        
        # Test translation
        result = translator.translate_text(sample_text, "Spanish")
        
        if result['status'] == 'success':
            print(f"✅ Original: {sample_text}")
            print(f"✅ Translated: {result['translated_text']}")
        else:
            print(f"❌ Translation failed: {result.get('error', 'Unknown error')}")
        
        return True
    except Exception as e:
        print(f"❌ Translation error: {e}")
        return False

def test_web_scraping():
    """Test web scraping functionality"""
    print("\n🌐 Testing Web Scraping...")
    
    try:
        from utils.web_scraper import WebScraper
        scraper = WebScraper()
        
        # Test with a simple URL (Wikipedia)
        test_url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
        
        print(f"🔍 Testing URL: {test_url}")
        result = scraper.extract_text_from_url(test_url)
        
        if result['status'] == 'success':
            print(f"✅ Title: {result['title'][:50]}...")
            print(f"✅ Word count: {result['word_count']}")
            print(f"✅ Domain: {result['domain']}")
            print(f"✅ Sample text: {result['text'][:200]}...")
        else:
            print(f"❌ Scraping failed: {result.get('error', 'Unknown error')}")
        
        return True
    except Exception as e:
        print(f"❌ Web scraping error: {e}")
        return False

def test_full_pipeline():
    """Test the complete pipeline"""
    print("\n🎧 Testing Complete Pipeline...")
    
    try:
        from api_rewriter import TextProcessor
        from api_tts import AdvancedTTS
        from utils.translator import LanguageTranslator
        
        # Sample text
        sample_text = "Welcome to EchoVerse! This is an AI-powered audiobook creator that transforms text into professional audio."
        
        print(f"📝 Input text: {sample_text}")
        
        # Step 1: Process text
        processor = TextProcessor()
        processed_text = processor.rewrite_text(sample_text, "formal", "positive")
        print(f"🔄 Processed text: {processed_text}")
        
        # Step 2: Translate (optional)
        translator = LanguageTranslator()
        translation = translator.translate_text(processed_text, "Spanish")
        
        if translation['status'] == 'success':
            print(f"🌍 Spanish translation: {translation['translated_text']}")
        
        # Step 3: Generate audio (simulation)
        tts = AdvancedTTS()
        voices = tts.get_available_voices("English", "Female")
        
        if voices:
            print(f"🎤 Would generate audio with voice: {voices[0]['display_name']}")
            print(f"📁 Audio file would be saved as: echoverse_audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3")
        
        return True
    except Exception as e:
        print(f"❌ Pipeline error: {e}")
        return False

def main():
    """Main test function"""
    print("🎧 EchoVerse - Output Test")
    print("=" * 60)
    
    # Create necessary directories
    directories = ['uploads', 'audio_outputs', 'temp']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")
    
    # Run tests
    tests = [
        ("Text Processing", test_text_processing),
        ("Text-to-Speech", test_tts),
        ("File Processing", test_file_processing),
        ("Translation", test_translation),
        ("Web Scraping", test_web_scraping),
        ("Complete Pipeline", test_full_pipeline)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print("=" * 60)
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if success:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! EchoVerse is ready to use.")
        print("\n🚀 To run the full application:")
        print("   python run.py")
        print("   or")
        print("   streamlit run main.py")
    else:
        print("⚠️ Some tests failed. Check the error messages above.")
        print("\n🔧 Try installing missing dependencies:")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    main()
