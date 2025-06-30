import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_elevenlabs_setup():
    """Test ElevenLabs API setup and configuration"""
    
    # Check if API key is set
    api_key = os.environ.get("ELEVEN_API_KEY")
    if not api_key:
        print("❌ ELEVEN_API_KEY environment variable is not set!")
        print("Please set your ElevenLabs API key in a .env file or as an environment variable")
        print("Example .env file content:")
        print("ELEVEN_API_KEY=your_api_key_here")
        return False
    
    print(f"✅ ELEVEN_API_KEY is set: {api_key[:10]}...")
    
    # Test ElevenLabs import
    try:
        import elevenlabs
        from elevenlabs.client import ElevenLabs
        print("✅ ElevenLabs package imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import ElevenLabs: {e}")
        print("Please install elevenlabs: pip install elevenlabs")
        return False
    
    # Test API connection
    try:
        client = ElevenLabs(api_key=api_key)
        # Try to get available voices to test API connection
        voices = client.voices.get_all()
        print(f"✅ ElevenLabs API connection successful! Found {len(voices.voices)} voices")
        return True
    except Exception as e:
        print(f"❌ ElevenLabs API connection failed: {e}")
        print("Please check your API key and internet connection")
        return False

if __name__ == "__main__":
    print("Testing ElevenLabs Setup...")
    print("=" * 40)
    test_elevenlabs_setup() 