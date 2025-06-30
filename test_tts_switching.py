#!/usr/bin/env python3
"""
Test script to demonstrate TTS switching between ElevenLabs and gTTS
"""

import os
from dotenv import load_dotenv
from ecommerce_voice_assistant import EcommerceVoiceAssistant

# Load environment variables
load_dotenv()

def test_tts_switching():
    """Test switching between TTS providers"""
    
    print("🎵 TTS Switching Test")
    print("=" * 40)
    
    # Initialize voice assistant with ElevenLabs
    assistant = EcommerceVoiceAssistant(tts_provider="elevenlabs")
    
    test_text = "Hello! This is a test of the text-to-speech switching functionality. You should hear different voices when we switch between providers."
    
    print(f"📝 Test text: {test_text}")
    print("\n" + "="*40)
    
    # Test ElevenLabs
    print("🎤 Testing ElevenLabs TTS...")
    try:
        audio_file = assistant.text_to_speech_elevenlabs(test_text, "test_elevenlabs.wav")
        if audio_file:
            print("✅ ElevenLabs audio generated successfully")
            print("🔊 Playing ElevenLabs audio...")
            assistant.play_audio(audio_file)
        else:
            print("❌ Failed to generate ElevenLabs audio")
    except Exception as e:
        print(f"❌ ElevenLabs error: {e}")
    
    print("\n" + "="*40)
    
    # Test gTTS
    print("🎤 Testing gTTS (Google)...")
    try:
        audio_file = assistant.text_to_speech_gtts(test_text, "test_gtts.wav")
        if audio_file:
            print("✅ gTTS audio generated successfully")
            print("🔊 Playing gTTS audio...")
            assistant.play_audio(audio_file)
        else:
            print("❌ Failed to generate gTTS audio")
    except Exception as e:
        print(f"❌ gTTS error: {e}")
    
    print("\n" + "="*40)
    
    # Test switching functionality
    print("🔄 Testing TTS switching...")
    
    # Start with ElevenLabs
    assistant.set_tts_provider("elevenlabs")
    print(f"🎵 Current provider: {assistant.tts_provider}")
    
    # Switch to gTTS
    assistant.set_tts_provider("gtts")
    print(f"🎵 Switched to: {assistant.tts_provider}")
    
    # Switch back to ElevenLabs
    assistant.set_tts_provider("elevenlabs")
    print(f"🎵 Switched back to: {assistant.tts_provider}")
    
    print("\n✅ TTS switching test completed!")

def test_command_line_options():
    """Test command line argument parsing"""
    print("\n🔧 Testing Command Line Options")
    print("=" * 40)
    
    print("To test different TTS providers from command line:")
    print("  python ecommerce_voice_assistant.py --tts elevenlabs")
    print("  python ecommerce_voice_assistant.py --tts gtts")
    print("\nOr use voice commands during conversation:")
    print("  'switch voice'")
    print("  'change voice'")
    print("  'switch tts'")

def main():
    """Main test function"""
    
    # Check if API keys are available
    if not os.environ.get("GROQ_API_KEY"):
        print("❌ GROQ_API_KEY not found in environment variables")
        print("Please set up your .env file with your API keys")
        return
    
    if not os.environ.get("ELEVEN_API_KEY"):
        print("⚠️  ELEVEN_API_KEY not found - ElevenLabs TTS will not work")
        print("You can still test gTTS functionality")
    
    try:
        # Run TTS switching test
        test_tts_switching()
        
        # Show command line options
        test_command_line_options()
        
        print("\n🎉 TTS switching test completed successfully!")
        print("\nNext steps:")
        print("1. Run voice assistant: python ecommerce_voice_assistant.py")
        print("2. Run web interface: python ecommerce_gradio_app.py")
        print("3. Try saying 'switch voice' during conversation")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        print("Please check your API keys and internet connection")

if __name__ == "__main__":
    main() 