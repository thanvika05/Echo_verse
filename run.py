#!/usr/bin/env python3
"""
EchoVerse Startup Script
Quick launcher for the EchoVerse AI Audiobook Creator
"""

import os
import sys
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit',
        'edge_tts',
        'requests',
        'beautifulsoup4',
        'PyPDF2',
        'docx',
        'googletrans',
        'pydub',
        'soundfile'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'docx':
                importlib.import_module('docx')
            else:
                importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Please install missing packages using:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def create_directories():
    """Create necessary directories"""
    directories = ['uploads', 'audio_outputs', 'temp']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")
        else:
            print(f"📁 Directory exists: {directory}")

def main():
    """Main startup function"""
    print("🎧 EchoVerse - AI Audiobook Creator")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    print("\n🔍 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    
    print("\n📁 Setting up directories...")
    create_directories()
    
    print("\n🚀 Starting EchoVerse...")
    print("📱 The application will open in your browser")
    print("🌐 URL: http://localhost:8501")
    print("\n" + "=" * 50)
    
    try:
        # Run Streamlit app
        subprocess.run([sys.executable, "-m", "streamlit", "run", "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 EchoVerse stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error starting EchoVerse: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("\n❌ Error: main.py not found")
        print("Please ensure you're running this script from the EchoVerse directory")
        sys.exit(1)

if __name__ == "__main__":
    main()
