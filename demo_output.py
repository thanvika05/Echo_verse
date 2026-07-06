#!/usr/bin/env python3
"""
EchoVerse Demo Output Script
Shows actual output and generates sample audio
"""

import os
import sys
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def demo_text_processing():
    """Demo text processing with output"""
    print("📝 TEXT PROCESSING DEMO")
    print("-" * 40)
    
    from api_rewriter import TextProcessor
    processor = TextProcessor()
    
    # Sample texts
    samples = [
        "Hey there! This is gonna be awesome!",
        "The weather is terrible today.",
        "I need to do stuff and things."
    ]
    
    for i, text in enumerate(samples, 1):
        print(f"\n{i}. Original: {text}")
        
        # Process with different styles
        formal = processor.rewrite_text(text, "formal", "professional")
        casual = processor.rewrite_text(text, "casual", "positive")
        
        print(f"   Formal: {formal}")
        print(f"   Casual: {casual}")
        
        # Analyze style
        analysis = processor.detect_text_style(text)
        print(f"   Analysis: Style={analysis['style']}, Words={analysis['word_count']}")

def demo_translation():
    """Demo translation with output"""
    print("\n🌍 TRANSLATION DEMO")
    print("-" * 40)
    
    from utils.translator import LanguageTranslator
    translator = LanguageTranslator()
    
    text = "Hello, welcome to EchoVerse! This is an amazing audiobook creator."
    
    languages = ["Spanish", "French", "German", "Hindi"]
    
    print(f"Original: {text}")
    
    for lang in languages:
        result = translator.translate_text(text, lang)
        if result['status'] == 'success':
            print(f"{lang}: {result['translated_text']}")
        else:
            print(f"{lang}: Translation failed")

def demo_voice_options():
    """Demo available voices"""
    print("\n🎤 VOICE OPTIONS DEMO")
    print("-" * 40)
    
    from api_tts import AdvancedTTS
    tts = AdvancedTTS()
    
    languages = ["English", "Spanish", "French", "German"]
    
    for lang in languages:
        print(f"\n{lang} Voices:")
        male_voices = tts.get_available_voices(lang, "Male")
        female_voices = tts.get_available_voices(lang, "Female")
        
        print(f"  Male: {len(male_voices)} voices")
        for voice in male_voices[:2]:  # Show first 2
            print(f"    - {voice['display_name']}")
        
        print(f"  Female: {len(female_voices)} voices")
        for voice in female_voices[:2]:  # Show first 2
            print(f"    - {voice['display_name']}")

def demo_audio_generation():
    """Demo actual audio generation"""
    print("\n🎧 AUDIO GENERATION DEMO")
    print("-" * 40)
    
    try:
        from api_tts import AdvancedTTS
        tts = AdvancedTTS()
        
        # Sample text
        sample_text = "Welcome to EchoVerse! This is a demonstration of AI-powered audiobook creation. Enjoy listening to this sample audio."
        
        print(f"Text to convert: {sample_text}")
        
        # Get available voices
        voices = tts.get_available_voices("English", "Female")
        if voices:
            voice_id = voices[0]['voice_id']
            print(f"Using voice: {voices[0]['display_name']}")
            
            # Generate audio
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"demo_audio_{timestamp}.mp3"
            
            print("Generating audio... (this may take a few seconds)")
            audio_path = tts.text_to_speech(
                text=sample_text,
                filename=filename,
                voice=voice_id,
                language="English"
            )
            
            if os.path.exists(audio_path):
                file_size = os.path.getsize(audio_path) / (1024 * 1024)
                print(f"✅ Audio generated successfully!")
                print(f"📁 File: {audio_path}")
                print(f"📊 Size: {file_size:.2f} MB")
                print(f"🎵 You can play this file to hear the output")
            else:
                print("❌ Audio generation failed")
        
    except Exception as e:
        print(f"❌ Audio generation error: {e}")

def demo_file_processing():
    """Demo file processing"""
    print("\n📁 FILE PROCESSING DEMO")
    print("-" * 40)
    
    from utils.file_processor import FileProcessor
    
    # Create a sample file
    sample_content = """
    Chapter 1: Introduction to EchoVerse
    
    EchoVerse is an innovative AI-powered audiobook creation tool that transforms 
    written content into professional audio narration. This revolutionary platform 
    combines advanced text processing, translation capabilities, and high-quality 
    text-to-speech technology to deliver exceptional audiobook experiences.
    
    Chapter 2: Key Features
    
    The platform offers multiple input methods including direct text input, 
    file uploads, and URL processing. Users can choose from various voice 
    options, adjust speech rates, and translate content into multiple languages.
    """
    
    test_file = "demo_sample.txt"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(sample_content)
    
    try:
        processor = FileProcessor()
        result = processor.process_file(test_file)
        
        print(f"📄 File: {result['file_name']}")
        print(f"📊 Size: {result['file_size']} bytes")
        print(f"📝 Words: {result['word_count']}")
        print(f"🔤 Characters: {result['char_count']}")
        print(f"📖 Paragraphs: {result['paragraph_count']}")
        print(f"⏱️ Reading time: {result['estimated_reading_time']} minutes")
        
        # Show sample of extracted text
        print(f"\n📄 Sample text:")
        print(f"'{result['text'][:200]}...'")
        
    except Exception as e:
        print(f"❌ File processing error: {e}")
    finally:
        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)

def demo_web_scraping():
    """Demo web scraping"""
    print("\n🌐 WEB SCRAPING DEMO")
    print("-" * 40)
    
    from utils.web_scraper import WebScraper
    
    # Test with a simple, reliable URL
    test_url = "https://httpbin.org/html"
    
    print(f"Testing URL: {test_url}")
    
    try:
        scraper = WebScraper()
        result = scraper.extract_text_from_url(test_url)
        
        if result['status'] == 'success':
            print(f"✅ Successfully extracted content")
            print(f"📄 Title: {result['title']}")
            print(f"📊 Words: {result['word_count']}")
            print(f"🔤 Characters: {result['char_count']}")
            print(f"🌐 Domain: {result['domain']}")
            
            # Show sample text
            sample_text = result['text'][:300] + "..." if len(result['text']) > 300 else result['text']
            print(f"\n📄 Sample content:")
            print(f"'{sample_text}'")
        else:
            print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    
    except Exception as e:
        print(f"❌ Web scraping error: {e}")

def main():
    """Main demo function"""
    print("🎧 EchoVerse - Output Demo")
    print("=" * 60)
    print("This demo shows the actual output of EchoVerse components")
    print("=" * 60)
    
    # Create directories
    for directory in ['uploads', 'audio_outputs', 'temp']:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    # Run demos
    demos = [
        demo_text_processing,
        demo_translation,
        demo_voice_options,
        demo_file_processing,
        demo_web_scraping,
        demo_audio_generation
    ]
    
    for demo in demos:
        try:
            demo()
            print("\n" + "=" * 60)
        except Exception as e:
            print(f"❌ Demo failed: {e}")
            print("\n" + "=" * 60)
    
    print("\n🎉 Demo completed!")
    print("\n📋 Summary of what you saw:")
    print("✅ Text processing with different styles")
    print("✅ Translation to multiple languages")
    print("✅ Available voice options")
    print("✅ File processing capabilities")
    print("✅ Web scraping functionality")
    print("✅ Actual audio generation")
    
    print("\n🚀 To run the full web application:")
    print("   python run.py")
    print("   or")
    print("   streamlit run main.py")

if __name__ == "__main__":
    main()
