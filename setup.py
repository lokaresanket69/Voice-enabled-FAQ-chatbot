#!/usr/bin/env python3
"""
Setup script for ShopSmart E-commerce Voice Assistant
This script helps users configure the chatbot and check their setup
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required. Current version:", sys.version)
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\n📦 Checking dependencies...")
    
    # Package name mapping (import name -> package name)
    package_mapping = {
        'groq': 'groq',
        'elevenlabs': 'elevenlabs',
        'streamlit': 'streamlit',
        'speech_recognition': 'speechrecognition',  # Note the underscore
        'pydub': 'pydub',
        'pyaudio': 'pyaudio',
        'numpy': 'numpy',
        'dotenv': 'python-dotenv'  # Import name is dotenv
    }
    
    missing_packages = []
    
    for import_name, package_name in package_mapping.items():
        try:
            __import__(import_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name} - Missing")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    print("\n🎬 Checking FFmpeg...")
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ FFmpeg is installed")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ FFmpeg not found")
    print("Please install FFmpeg:")
    system = platform.system()
    if system == "Darwin":  # macOS
        print("  brew install ffmpeg")
    elif system == "Linux":
        print("  sudo apt install ffmpeg")
    elif system == "Windows":
        print("  Download from: https://ffmpeg.org/download.html")
    
    return False

def check_api_keys():
    """Check if API keys are configured"""
    print("\n🔑 Checking API keys...")
    
    # Load .env file if it exists
    env_file = ".env"
    if os.path.exists(env_file):
        # Load environment variables from .env file
        from dotenv import load_dotenv
        load_dotenv()
        
        groq_key = os.environ.get("GROQ_API_KEY")
        elevenlabs_key = os.environ.get("ELEVEN_API_KEY")
        
        if groq_key and groq_key != "your_groq_api_key_here":
            print("✅ GROQ_API_KEY found")
        else:
            print("❌ GROQ_API_KEY missing or not set")
            
        if elevenlabs_key and elevenlabs_key != "your_elevenlabs_api_key_here":
            print("✅ ELEVEN_API_KEY found")
        else:
            print("❌ ELEVEN_API_KEY missing or not set")
            
        return (groq_key and groq_key != "your_groq_api_key_here" and 
                elevenlabs_key and elevenlabs_key != "your_elevenlabs_api_key_here")
    else:
        print("❌ .env file not found")
        return False

def create_env_file():
    """Create .env file template"""
    print("\n📝 Creating .env file template...")
    
    env_content = """# ShopSmart E-commerce Voice Assistant Configuration
# Get your API keys from:
# Groq: https://console.groq.com/
# ElevenLabs: https://elevenlabs.io/

GROQ_API_KEY=your_groq_api_key_here
ELEVEN_API_KEY=your_elevenlabs_api_key_here
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("✅ .env file created")
    print("⚠️  Please edit .env file with your actual API keys")

def run_quick_test():
    """Run a quick test to verify everything works"""
    print("\n🧪 Running quick test...")
    
    try:
        # Load environment variables from .env file
        from dotenv import load_dotenv
        load_dotenv()
        
        from ecommerce_brain import EcommerceChatbot
        from conversation_database import ConversationDatabase
        
        # Test database
        db = ConversationDatabase()
        print("✅ Database connection successful")
        
        # Test chatbot with conversation history
        chatbot = EcommerceChatbot()
        chatbot.start_new_conversation("Test Session", "Testing conversation history")
        response = chatbot.get_response("Hello")
        print("✅ Chatbot with conversation history test successful")
        return True
    except Exception as e:
        print(f"❌ Chatbot test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🛍️ ShopSmart E-commerce Voice Assistant Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Check dependencies
    if not check_dependencies():
        print("\n💡 To install dependencies, run:")
        print("   pip install -r requirements.txt")
        return False
    
    # Check FFmpeg
    ffmpeg_ok = check_ffmpeg()
    
    # Check API keys
    api_keys_ok = check_api_keys()
    
    if not api_keys_ok:
        print("\n🔧 Setting up API keys...")
        create_env_file()
        print("\n📋 Next steps:")
        print("1. Get your API keys:")
        print("   - Groq: https://console.groq.com/")
        print("   - ElevenLabs: https://elevenlabs.io/")
        print("2. Edit the .env file with your keys")
        print("3. Run this setup script again")
        return False
    
    # Run quick test
    if not run_quick_test():
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\n🚀 You can now run:")
    print("   python ecommerce_voice_assistant.py  # Voice assistant")
    print("   python -m streamlit run ecommerce_streamlit_app.py  # Web interface")
    print("   python test_ecommerce_chatbot.py     # Test script")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Setup incomplete. Please fix the issues above and try again.")
        sys.exit(1) 