from dotenv import load_dotenv
load_dotenv()

import os
import gradio as gr
import logging
from ecommerce_brain import EcommerceChatbot
from ecommerce_voice_assistant import EcommerceVoiceAssistant

# Setup logging
logging.basicConfig(level=logging.INFO)

class EcommerceGradioApp:
    def __init__(self):
        self.chatbot = EcommerceChatbot()
        self.voice_assistant = EcommerceVoiceAssistant()
        self.conversation_history = []
        
    def process_text_input(self, user_message, history):
        """Process text input and return response"""
        if not user_message.strip():
            return "", history
            
        try:
            # Generate response
            bot_response = self.chatbot.get_response(user_message)
            
            # Add to history
            history.append([user_message, bot_response])
            
            return "", history
            
        except Exception as e:
            logging.error(f"Error processing text input: {e}")
            error_response = "I'm sorry, I'm having trouble processing your request right now. Could you try again?"
            history.append([user_message, error_response])
            return "", history
    
    def process_voice_input(self, audio_filepath, tts_provider):
        """Process voice input and return response"""
        if not audio_filepath:
            return "No audio input provided", None, []
            
        try:
            # Set TTS provider
            self.voice_assistant.set_tts_provider(tts_provider)
            
            # Transcribe audio
            transcribed_text = self.voice_assistant.transcribe_audio(audio_filepath)
            
            if not transcribed_text:
                return "Could not understand your speech. Please try again.", None, []
            
            # Generate response
            bot_response = self.chatbot.get_response(transcribed_text)
            
            # Convert response to speech
            response_audio = self.voice_assistant.text_to_speech(bot_response, "gradio_response.wav")
            
            # Create conversation history for display
            history = [[transcribed_text, bot_response]]
            
            return transcribed_text, response_audio, history
            
        except Exception as e:
            logging.error(f"Error processing voice input: {e}")
            error_response = "I'm sorry, I'm having trouble processing your voice input right now. Could you try again?"
            return "Error processing audio", None, [[transcribed_text if 'transcribed_text' in locals() else "Audio input", error_response]]
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        return []
    
    def create_interface(self):
        """Create the Gradio interface"""
        
        # Custom CSS for better styling
        css = """
        .gradio-container {
            max-width: 1200px !important;
            margin: auto !important;
        }
        .chat-container {
            border-radius: 15px;
            border: 2px solid #e0e0e0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            margin-bottom: 20px;
        }
        .user-message {
            background: #007bff;
            color: white;
            padding: 10px 15px;
            border-radius: 20px;
            margin: 5px 0;
            max-width: 80%;
            margin-left: auto;
        }
        .bot-message {
            background: #f8f9fa;
            color: #333;
            padding: 10px 15px;
            border-radius: 20px;
            margin: 5px 0;
            max-width: 80%;
        }
        .header {
            text-align: center;
            color: white;
            margin-bottom: 20px;
        }
        .feature-box {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            color: white;
        }
        .tts-selector {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            padding: 10px;
            margin: 10px 0;
        }
        """
        
        with gr.Blocks(css=css, title="ShopSmart E-commerce Voice Assistant") as interface:
            
            # Header
            with gr.Row():
                gr.HTML("""
                <div class="header">
                    <h1>🛍️ ShopSmart Voice Assistant</h1>
                    <p>Meet Alex, your friendly AI shopping assistant! 💬</p>
                </div>
                """)
            
            # Main content area
            with gr.Row():
                with gr.Column(scale=2):
                    # Chat interface
                    chatbot = gr.Chatbot(
                        label="💬 Chat with Alex",
                        height=400,
                        show_label=True,
                        container=True,
                        bubble_full_width=False
                    )
                    
                    # Text input
                    with gr.Row():
                        text_input = gr.Textbox(
                            placeholder="Type your message here...",
                            label="💬 Text Input",
                            lines=2,
                            scale=4
                        )
                        text_submit_btn = gr.Button("Send", variant="primary", scale=1)
                    
                    # Voice input section
                    with gr.Row():
                        with gr.Column(scale=3):
                            voice_input = gr.Audio(
                                sources=["microphone"],
                                type="filepath",
                                label="🎤 Voice Input"
                            )
                        with gr.Column(scale=1):
                            # TTS Provider Selection
                            tts_provider = gr.Dropdown(
                                choices=["ElevenLabs", "gTTS (Google)"],
                                value="ElevenLabs",
                                label="🎵 Voice Provider",
                                info="Choose your preferred voice"
                            )
                    
                    # Voice submit button
                    with gr.Row():
                        voice_submit_btn = gr.Button("Send Voice", variant="secondary", size="lg")
                    
                    # Clear button
                    clear_btn = gr.Button("🗑️ Clear Chat", variant="stop")
                
                with gr.Column(scale=1):
                    # Features and help
                    gr.HTML("""
                    <div class="feature-box">
                        <h3>🎯 What I can help with:</h3>
                        <ul>
                            <li>📱 Product recommendations</li>
                            <li>💰 Price comparisons</li>
                            <li>📦 Order tracking</li>
                            <li>🔄 Return policies</li>
                            <li>💳 Payment options</li>
                            <li>🚚 Shipping information</li>
                        </ul>
                    </div>
                    """)
                    
                    gr.HTML("""
                    <div class="feature-box">
                        <h3>🎵 Voice Options:</h3>
                        <ul>
                            <li><strong>ElevenLabs:</strong> More natural, human-like voice</li>
                            <li><strong>gTTS (Google):</strong> Clear, reliable voice</li>
                            <li>Switch between them anytime!</li>
                        </ul>
                    </div>
                    """)
                    
                    gr.HTML("""
                    <div class="feature-box">
                        <h3>💡 Quick Tips:</h3>
                        <ul>
                            <li>🎤 Use voice for hands-free shopping</li>
                            <li>💬 Type for detailed questions</li>
                            <li>🔍 Be specific about what you're looking for</li>
                            <li>❓ Ask follow-up questions</li>
                        </ul>
                    </div>
                    """)
                    
                    # Sample questions
                    gr.HTML("""
                    <div class="feature-box">
                        <h3>💭 Try asking:</h3>
                        <ul>
                            <li>"Show me smartphones under $1000"</li>
                            <li>"What's your return policy?"</li>
                            <li>"I need a laptop for gaming"</li>
                            <li>"How long does shipping take?"</li>
                        </ul>
                    </div>
                    """)
            
            # Event handlers
            text_submit_btn.click(
                fn=self.process_text_input,
                inputs=[text_input, chatbot],
                outputs=[text_input, chatbot]
            )
            
            text_input.submit(
                fn=self.process_text_input,
                inputs=[text_input, chatbot],
                outputs=[text_input, chatbot]
            )
            
            voice_submit_btn.click(
                fn=self.process_voice_input,
                inputs=[voice_input, tts_provider],
                outputs=[text_input, voice_input, chatbot]
            )
            
            clear_btn.click(
                fn=self.clear_history,
                outputs=[chatbot]
            )
            
            # Welcome message
            welcome_message = "Hi there! 👋 I'm Alex, your friendly shopping assistant at ShopSmart. I'm here to help you find the perfect products, answer questions about orders, or assist with anything else you need. What can I help you with today?"
            chatbot.value = [[None, welcome_message]]
        
        return interface

def main():
    """Main function to run the Gradio app"""
    app = EcommerceGradioApp()
    interface = app.create_interface()
    
    # Launch the app
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True,
        show_error=True
    )

if __name__ == "__main__":
    main() 