import os
import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import numpy as np
import subprocess
import platform
from groq import Groq
import elevenlabs
from elevenlabs.client import ElevenLabs
from gtts import gTTS
from ecommerce_brain import EcommerceChatbot

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EcommerceVoiceAssistant:
    def __init__(self, tts_provider="elevenlabs"):
        self.groq_api_key = os.environ.get("GROQ_API_KEY")
        self.elevenlabs_api_key = os.environ.get("ELEVEN_API_KEY")
        self.stt_model = "whisper-large-v3"
        
        # Initialize components
        self.groq_client = Groq(api_key=self.groq_api_key)
        self.elevenlabs_client = ElevenLabs(api_key=self.elevenlabs_api_key)
        self.chatbot = EcommerceChatbot()
        
        # TTS provider selection
        self.tts_provider = tts_provider.lower()
        
        # Voice settings
        self.voice_name = "Aria"  # ElevenLabs voice
        self.voice_model = "eleven_turbo_v2"
        
        # gTTS settings
        self.gtts_language = "en"
        self.gtts_slow = False
        
        logging.info(f"🎤 TTS Provider: {self.tts_provider}")
        
    def set_tts_provider(self, provider):
        """Change TTS provider on the fly"""
        provider = provider.lower()
        if provider in ["elevenlabs", "eleven", "11"]:
            self.tts_provider = "elevenlabs"
            logging.info("🎤 Switched to ElevenLabs TTS")
        elif provider in ["gtts", "google", "gt"]:
            self.tts_provider = "gtts"
            logging.info("🎤 Switched to gTTS (Google)")
        else:
            logging.warning(f"Unknown TTS provider: {provider}. Using ElevenLabs.")
            self.tts_provider = "elevenlabs"
        
    def record_audio(self, file_path="temp_audio.wav", timeout=10, phrase_time_limit=8):
        """
        Record audio from microphone and save as WAV file
        """
        recognizer = sr.Recognizer()
        
        try:
            with sr.Microphone() as source:
                logging.info("🎤 Adjusting for ambient noise...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                logging.info("🎤 Start speaking now...")
                
                # Record the audio
                audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                logging.info("✅ Recording complete.")
                
                # Convert to WAV file
                wav_data = audio_data.get_wav_data()
                audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
                audio_segment.export(file_path, format="wav", bitrate="128k")
                
                logging.info(f"💾 Audio saved to {file_path}")
                return file_path

        except sr.WaitTimeoutError:
            logging.warning("⏰ No speech detected within timeout period")
            return None
        except Exception as e:
            logging.error(f"❌ Error recording audio: {e}")
            return None

    def transcribe_audio(self, audio_filepath):
        """
        Convert speech to text using Groq's Whisper model
        """
        try:
            with open(audio_filepath, "rb") as audio_file:
                transcription = self.groq_client.audio.transcriptions.create(
                    model=self.stt_model,
                    file=audio_file,
                    language="en"
                )
            
            transcribed_text = transcription.text.strip()
            logging.info(f"📝 Transcribed: '{transcribed_text}'")
            return transcribed_text
            
        except Exception as e:
            logging.error(f"❌ Error transcribing audio: {e}")
            return None

    def generate_response(self, user_message):
        """
        Generate chatbot response using the e-commerce brain
        """
        try:
            response = self.chatbot.get_response(user_message)
            logging.info(f"🤖 Bot response: '{response}'")
            return response
        except Exception as e:
            logging.error(f"❌ Error generating response: {e}")
            return "I'm sorry, I'm having trouble processing your request right now. Could you try again?"

    def text_to_speech_gtts(self, text, output_filepath="response.wav"):
        """
        Convert text to speech using gTTS (Google Text-to-Speech)
        """
        try:
            # Create gTTS object
            tts = gTTS(text=text, lang=self.gtts_language, slow=self.gtts_slow)
            
            # Save as MP3 first
            mp3_path = output_filepath.replace(".wav", ".mp3")
            tts.save(mp3_path)
            
            # Convert MP3 to WAV using pydub
            try:
                audio = AudioSegment.from_mp3(mp3_path)
                audio.export(output_filepath, format="wav")
                
                # Clean up MP3 file
                if os.path.exists(mp3_path):
                    os.remove(mp3_path)
                
                logging.info(f"🔊 gTTS audio saved to {output_filepath}")
                return output_filepath
                
            except Exception as e:
                logging.error(f"❌ Error converting MP3 to WAV: {e}")
                return None
                
        except Exception as e:
            logging.error(f"❌ Error generating gTTS speech: {e}")
            return None

    def text_to_speech_elevenlabs(self, text, output_filepath="response.wav"):
        """
        Convert text to speech using ElevenLabs
        """
        try:
            audio = self.elevenlabs_client.generate(
                text=text,
                voice=self.voice_name,
                output_format="pcm_22050",
                model=self.voice_model
            )
            
            # Save the raw PCM data
            elevenlabs.save(audio, "temp_pcm.raw")
            
            # Convert PCM to WAV using pydub
            try:
                with open("temp_pcm.raw", "rb") as f:
                    pcm_data = f.read()
                
                # Convert to numpy array
                audio_array = np.frombuffer(pcm_data, dtype=np.int16)
                
                # Create AudioSegment from numpy array
                audio_segment = AudioSegment(
                    audio_array.tobytes(), 
                    frame_rate=22050,
                    sample_width=2,  # 16-bit
                    channels=1
                )
                
                # Export as WAV
                audio_segment.export(output_filepath, format="wav")
                
                # Clean up temp file
                if os.path.exists("temp_pcm.raw"):
                    os.remove("temp_pcm.raw")
                
                logging.info(f"🔊 ElevenLabs audio saved to {output_filepath}")
                return output_filepath
                
            except Exception as e:
                logging.error(f"❌ Error converting PCM to WAV: {e}")
                return None
                
        except Exception as e:
            logging.error(f"❌ Error generating ElevenLabs speech: {e}")
            return None

    def text_to_speech(self, text, output_filepath="response.wav"):
        """
        Convert text to speech using the selected provider
        """
        if self.tts_provider == "elevenlabs":
            return self.text_to_speech_elevenlabs(text, output_filepath)
        elif self.tts_provider == "gtts":
            return self.text_to_speech_gtts(text, output_filepath)
        else:
            logging.warning(f"Unknown TTS provider: {self.tts_provider}. Using ElevenLabs.")
            return self.text_to_speech_elevenlabs(text, output_filepath)

    def play_audio(self, audio_filepath):
        """
        Play audio file based on operating system
        """
        os_name = platform.system()
        try:
            if os_name == "Darwin":  # macOS
                subprocess.run(['afplay', audio_filepath])
            elif os_name == "Windows":  # Windows
                subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{audio_filepath}").PlaySync();'])
            elif os_name == "Linux":  # Linux
                subprocess.run(['aplay', audio_filepath])
            else:
                raise OSError("Unsupported operating system")
                
            logging.info("🔊 Audio played successfully")
            
        except Exception as e:
            logging.error(f"❌ Error playing audio: {e}")

    def conversation_loop(self):
        """
        Main conversation loop for voice interaction
        """
        print("🎉 Welcome to ShopSmart Voice Assistant!")
        print("🎤 I'm Alex, your friendly shopping assistant. How can I help you today?")
        print("💡 You can ask me about products, prices, shipping, returns, or anything else!")
        print("🎵 TTS Provider:", self.tts_provider.upper())
        print("🔇 Say 'goodbye' or 'exit' to end our conversation.")
        print("🎤 Say 'switch voice' to change TTS provider.")
        print("-" * 60)
        
        # Generate and play welcome message
        welcome_text = "Hi there! I'm Alex, your friendly shopping assistant at ShopSmart. I'm here to help you find the perfect products, answer questions about orders, or assist with anything else you need. What can I help you with today?"
        welcome_audio = self.text_to_speech(welcome_text, "welcome.wav")
        if welcome_audio:
            self.play_audio(welcome_audio)
        
        conversation_count = 0
        
        while True:
            try:
                # Record user input
                print("\n🎤 Listening... (speak now)")
                audio_file = self.record_audio()
                
                if not audio_file:
                    print("❌ No audio detected. Please try again.")
                    continue
                
                # Transcribe speech to text
                user_message = self.transcribe_audio(audio_file)
                
                if not user_message:
                    print("❌ Could not understand your speech. Please try again.")
                    continue
                
                # Check for exit commands
                if any(phrase in user_message.lower() for phrase in ['goodbye', 'exit', 'quit', 'bye', 'stop']):
                    print("👋 Goodbye! Thanks for shopping with ShopSmart!")
                    goodbye_text = "Thanks for chatting with me! Have a great day and happy shopping!"
                    goodbye_audio = self.text_to_speech(goodbye_text, "goodbye.wav")
                    if goodbye_audio:
                        self.play_audio(goodbye_audio)
                    break
                
                # Check for voice switching commands
                if any(phrase in user_message.lower() for phrase in ['switch voice', 'change voice', 'switch tts', 'change tts']):
                    current_provider = self.tts_provider
                    if current_provider == "elevenlabs":
                        self.set_tts_provider("gtts")
                        switch_message = "Switched to Google Text-to-Speech. You'll notice a different voice now!"
                    else:
                        self.set_tts_provider("elevenlabs")
                        switch_message = "Switched to ElevenLabs. You'll hear a more natural voice now!"
                    
                    print(f"🎵 {switch_message}")
                    switch_audio = self.text_to_speech(switch_message, "switch_voice.wav")
                    if switch_audio:
                        self.play_audio(switch_audio)
                    continue
                
                print(f"👤 You said: {user_message}")
                
                # Generate bot response
                bot_response = self.generate_response(user_message)
                print(f"🤖 Alex: {bot_response}")
                
                # Convert response to speech and play
                response_audio = self.text_to_speech(bot_response, f"response_{conversation_count}.wav")
                if response_audio:
                    self.play_audio(response_audio)
                
                conversation_count += 1
                
                # Clean up audio files
                if os.path.exists(audio_file):
                    os.remove(audio_file)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye! Thanks for using ShopSmart Voice Assistant!")
                break
            except Exception as e:
                logging.error(f"❌ Unexpected error: {e}")
                print("❌ Something went wrong. Please try again.")

def main():
    """
    Main function to run the voice assistant
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='ShopSmart E-commerce Voice Assistant')
    parser.add_argument('--tts', choices=['elevenlabs', 'gtts'], default='elevenlabs',
                       help='Choose TTS provider (default: elevenlabs)')
    
    args = parser.parse_args()
    
    assistant = EcommerceVoiceAssistant(tts_provider=args.tts)
    assistant.conversation_loop()

if __name__ == "__main__":
    main() 