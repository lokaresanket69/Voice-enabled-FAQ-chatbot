import streamlit as st
import os
import tempfile
import logging
from dotenv import load_dotenv
from ecommerce_brain import EcommerceChatbot
from ecommerce_voice_assistant import EcommerceVoiceAssistant
import time
import sqlite3

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)

# Page configuration
st.set_page_config(
    page_title="ShopSmart Voice Assistant",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        max-width: 80%;
    }
    
    .user-message {
        background: #007bff;
        color: white;
        margin-left: auto;
        text-align: right;
    }
    
    .bot-message {
        background: #f8f9fa;
        color: #333;
        border: 1px solid #e0e0e0;
    }
    
    .feature-box {
        background: #222c3c;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        color: #fff;
    }
    
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
    }
    
    .voice-section {
        background: rgba(102, 126, 234, 0.05);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #e0e0e0;
        margin: 1rem 0;
    }
    
    .chat-container {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        border: 2px solid #e0e0e0;
        min-height: 400px;
        max-height: 600px;
        overflow-y: auto;
    }
    
    .status-message {
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        font-weight: bold;
    }
    
    .status-success {
        background: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .status-error {
        background: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    
    .status-info {
        background: #d1ecf1;
        color: #0c5460;
        border: 1px solid #bee5eb;
    }
    
    .conversation-item {
        background: #222c3c;
        border-radius: 8px;
        padding: 0.75rem;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        cursor: pointer;
        transition: all 0.3s ease;
        color: #fff;
        font-weight: 600;
    }
    
    .conversation-item small {
        color: #b0b8c1;
    }
    
    .conversation-item:hover {
        background: #2d3a4d;
        transform: translateX(5px);
    }
    
    .conversation-item.active {
        background: #667eea;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_app():
    """Load and cache the main app class to preserve state across reruns"""
    logging.info("🚀 Initializing ShopSmart App...")
    return EcommerceStreamlitApp()

class EcommerceStreamlitApp:
    def __init__(self):
        self.chatbot = EcommerceChatbot()
        self.voice_assistant = EcommerceVoiceAssistant()
        
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'tts_provider' not in st.session_state:
            st.session_state.tts_provider = "ElevenLabs"
        if 'audio_response' not in st.session_state:
            st.session_state.audio_response = None
        if 'is_recording' not in st.session_state:
            st.session_state.is_recording = False
        if 'voice_status' not in st.session_state:
            st.session_state.voice_status = None
        if 'current_conversation_id' not in st.session_state:
            st.session_state.current_conversation_id = None
        if 'conversations_loaded' not in st.session_state:
            st.session_state.conversations_loaded = False
            
    def process_text_input(self, user_message):
        """Process text input and return response"""
        if not user_message.strip():
            return None
            
        try:
            # Generate response using chatbot with conversation context
            bot_response = self.chatbot.get_response(user_message)
            return bot_response
            
        except Exception as e:
            logging.error(f"Error processing text input: {e}")
            return "I'm sorry, I'm having trouble processing your request right now. Could you try again?"
    
    def process_voice_input(self, audio_file, tts_provider):
        """Process voice input and return response"""
        if audio_file is None:
            return None, None, None
            
        try:
            # Set TTS provider
            self.voice_assistant.set_tts_provider(tts_provider)
            
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(audio_file.read())
                tmp_file_path = tmp_file.name
            
            # Transcribe audio
            transcribed_text = self.voice_assistant.transcribe_audio(tmp_file_path)
            
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
            if not transcribed_text:
                return "Could not understand your speech. Please try again.", None, None
            
            # Generate response using chatbot with conversation context
            bot_response = self.chatbot.get_response(transcribed_text)
            
            # Convert response to speech
            response_audio_path = self.voice_assistant.text_to_speech(bot_response, "streamlit_response.wav")
            
            return transcribed_text, bot_response, response_audio_path
            
        except Exception as e:
            logging.error(f"Error processing voice input: {e}")
            return "Error processing audio", "I'm sorry, I'm having trouble processing your voice input right now. Could you try again?", None
    
    def record_audio_from_microphone(self, tts_provider):
        """Record audio from microphone and process"""
        try:
            # Set TTS provider
            self.voice_assistant.set_tts_provider(tts_provider)
            
            # Record audio
            audio_file_path = self.voice_assistant.record_audio("temp_streamlit_audio.wav")
            
            if not audio_file_path or not os.path.exists(audio_file_path):
                return "No audio recorded. Please try again.", None, None
            
            # Transcribe audio
            transcribed_text = self.voice_assistant.transcribe_audio(audio_file_path)
            
            if not transcribed_text:
                return "Could not understand your speech. Please try again.", None, None
            
            # Generate response using chatbot with conversation context
            bot_response = self.chatbot.get_response(transcribed_text)
            
            # Convert response to speech
            response_audio_path = self.voice_assistant.text_to_speech(bot_response, "streamlit_response.wav")
            
            # Clean up temp audio file
            if os.path.exists(audio_file_path):
                os.unlink(audio_file_path)
            
            return transcribed_text, bot_response, response_audio_path
            
        except Exception as e:
            logging.error(f"Error recording from microphone: {e}")
            return "Error recording audio. Please try again.", None, None
    
    def display_chat_message(self, role, content):
        """Display a chat message with proper styling"""
        if role == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>You:</strong> {content}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message bot-message">
                <strong>Alex:</strong> {content}
            </div>
            """, unsafe_allow_html=True)
    
    def display_status_message(self, message, status_type="info"):
        """Display a status message"""
        css_class = f"status-{status_type}"
        st.markdown(f"""
        <div class="status-message {css_class}">
            {message}
        </div>
        """, unsafe_allow_html=True)
    
    def load_conversation_messages(self, conversation_id):
        """Load messages for a given conversation ID"""
        try:
            conversation = self.chatbot.load_conversation(conversation_id)
            if conversation:
                st.session_state.messages = conversation['messages']
                st.session_state.current_conversation_id = conversation_id
                self.display_status_message(f"Successfully loaded conversation: {conversation['title']}", "success")
            else:
                st.session_state.messages = []
                self.display_status_message("Could not find conversation.", "error")
        except Exception as e:
            logging.error(f"Error loading conversation {conversation_id}: {e}")
            self.display_status_message("An error occurred while loading the conversation.", "error")
    
    def smart_auto_title(self, conversation):
        """Auto-title a conversation based on its content."""
        # Use keywords or generate a summary
        keywords = ["refund", "return", "order", "payment", "shipping", "cancel", "exchange"]
        product_keywords = ["iphone", "samsung", "laptop", "macbook", "jeans", "shirt", "coffee", "blender"]
        user_msgs = [msg['content'].lower() for msg in conversation['messages'] if msg['role'] == 'user']
        all_text = " ".join(user_msgs)
        for word in keywords:
            if word in all_text:
                return word.capitalize()
        for word in product_keywords:
            if word in all_text:
                return word.capitalize()
        # If long, summarize (simple: first 6 words)
        if len(all_text.split()) > 6:
            return " ".join(all_text.split()[:6]) + "..."
        return "General Inquiry"

    def update_conversation_title(self, conversation_id, new_title):
        self.chatbot.db.update_conversation_summary(conversation_id, new_title)
        # Also update the title in the conversations table
        with sqlite3.connect(self.chatbot.db.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE conversations SET title = ? WHERE conversation_id = ?", (new_title, conversation_id))
            conn.commit()

    def create_interface(self):
        """Create the Streamlit interface"""
        
        # Initialize session state
        self.initialize_session_state()
        
        # Header
        st.markdown("""
        <div class="main-header">
            <h1>🛍️ ShopSmart Voice Assistant</h1>
            <p>Meet Alex, your friendly AI shopping assistant! 💬</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Main layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 💬 Chat with Alex")
            
            # Conversation management section
            with st.expander("📚 Conversation History", expanded=False):
                col_conv1, col_conv2 = st.columns([3, 1])
                
                with col_conv1:
                    # Search conversations
                    search_query = st.text_input("Search conversations:", placeholder="Type to search...")
                    
                with col_conv2:
                    if st.button("🔍 Search", type="secondary"):
                        if search_query:
                            conversations = self.chatbot.search_conversations(search_query)
                        else:
                            conversations = self.chatbot.list_conversations(10)
                    else:
                        conversations = self.chatbot.list_conversations(10)
                
                # Display conversations
                if conversations:
                    st.markdown("#### Recent Conversations:")
                    for conv in conversations:
                        conv_key = f"conv_{conv['conversation_id']}"
                        is_active = st.session_state.current_conversation_id == conv['conversation_id']
                        # Smart auto-title if needed
                        display_title = conv['title']
                        if not display_title or display_title.startswith("ShopSmart Session"):
                            # Try to auto-title
                            loaded_conv = self.chatbot.db.get_conversation(conv['conversation_id'])
                            display_title = self.smart_auto_title(loaded_conv)
                            self.update_conversation_title(conv['conversation_id'], display_title)
                        with st.container():
                            col_info, col_load = st.columns([4, 1])
                            with col_info:
                                st.markdown(f"""
                                <div class="conversation-item {'active' if is_active else ''}">
                                    <strong>{display_title}</strong><br>
                                    <small>📅 {conv['updated_at']} | 💬 {conv['message_count']} messages</small>
                                    {f"<br><small>🏷️ {', '.join(conv['tags'])}</small>" if conv['tags'] else ""}
                                </div>
                                """, unsafe_allow_html=True)
                            with col_load:
                                if st.button("Load", key=f"load_{conv_key}", type="primary" if is_active else "secondary"):
                                    if self.load_conversation_messages(conv['conversation_id']):
                                        st.success(f"✅ Loaded conversation: {display_title}")
                                        st.rerun()
                        # Manual title edit
                        if is_active:
                            with st.form(f"edit_title_form_{conv['conversation_id']}", clear_on_submit=True):
                                new_title = st.text_input("Edit conversation title:", value=display_title, key=f"edit_title_{conv['conversation_id']}")
                                if st.form_submit_button("Save Title"):
                                    self.update_conversation_title(conv['conversation_id'], new_title)
                                    st.success("Title updated!")
                                    st.rerun()
                else:
                    st.info("No conversations found. Start chatting to create your first conversation!")
                
                # New conversation button
                if st.button("🆕 Start New Conversation", type="primary"):
                    self.chatbot.start_new_conversation()
                    st.session_state.current_conversation_id = self.chatbot.current_conversation_id
                    st.session_state.messages = []
                    st.success("✅ Started new conversation!")
                    st.rerun()
            
            # Current conversation info
            if st.session_state.current_conversation_id:
                summary = self.chatbot.get_conversation_summary()
                # Fix: summary can be a string or dict
                if isinstance(summary, dict):
                    st.markdown(f"""
                    <div class="feature-box">
                        <strong>Current Conversation:</strong> {summary.get('title', 'Untitled')}<br>
                        <small>💬 {summary.get('message_count', 0)} messages | 📅 {summary.get('updated_at', '')}</small>
                    </div>
                    """, unsafe_allow_html=True)
                elif isinstance(summary, str):
                    st.markdown(f"""
                    <div class="feature-box">
                        <strong>Current Conversation:</strong> {summary}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Chat container
            chat_container = st.container()
            
            with chat_container:
                # Display chat messages
                for message in st.session_state.messages:
                    self.display_chat_message(message["role"], message["content"])
            
            # Text input section
            st.markdown("### 💬 Text Input")
            with st.form("text_input_form"):
                text_input = st.text_area(
                    "Type your message here...",
                    placeholder="Ask me about products, orders, or anything else!",
                    height=100
                )
                text_submit = st.form_submit_button("Send Message", type="primary")
            
            # Voice input section
            st.markdown("### 🎤 Voice Input")
            
            # Voice input options
            voice_option = st.radio(
                "Choose voice input method:",
                ["🎙️ Record from Microphone", "📁 Upload Audio File"],
                horizontal=True
            )
            
            if voice_option == "🎙️ Record from Microphone":
                # Microphone recording
                col_voice1, col_voice2 = st.columns([3, 1])
                
                with col_voice1:
                    if st.button("🎤 Start Recording", type="primary", key="record_btn"):
                        st.session_state.is_recording = True
                        st.session_state.voice_status = "Recording... Please speak now!"
                        st.rerun()
                
                with col_voice2:
                    tts_provider = st.selectbox(
                        "Voice Provider",
                        ["ElevenLabs", "gTTS (Google)"],
                        index=0 if st.session_state.tts_provider == "ElevenLabs" else 1,
                        key="tts_mic"
                    )
                
                # Show recording status
                if st.session_state.voice_status:
                    self.display_status_message(st.session_state.voice_status, "info")
                
                # Process recording if active
                if st.session_state.is_recording:
                    with st.spinner("🎤 Recording and processing..."):
                        transcribed_text, bot_response, audio_response_path = self.record_audio_from_microphone(tts_provider)
                        
                        if transcribed_text and bot_response:
                            # Add messages to chat
                            st.session_state.messages.append({"role": "user", "content": f"[Voice] {transcribed_text}"})
                            st.session_state.messages.append({"role": "assistant", "content": bot_response})
                            
                            # Store audio response path
                            if audio_response_path:
                                st.session_state.audio_response = audio_response_path
                            
                            st.session_state.voice_status = "✅ Voice processed successfully!"
                        else:
                            st.session_state.voice_status = f"❌ {transcribed_text}"
                        
                        st.session_state.is_recording = False
                        st.rerun()
            
            else:
                # File upload
                with st.form("voice_input_form"):
                    col_voice1, col_voice2 = st.columns([3, 1])
                    
                    with col_voice1:
                        audio_file = st.file_uploader(
                            "Upload audio file",
                            type=['wav', 'mp3', 'm4a'],
                            help="Upload an audio file (WAV, MP3, or M4A)"
                        )
                    
                    with col_voice2:
                        tts_provider = st.selectbox(
                            "Voice Provider",
                            ["ElevenLabs", "gTTS (Google)"],
                            index=0 if st.session_state.tts_provider == "ElevenLabs" else 1,
                            key="tts_upload"
                        )
                    
                    voice_submit = st.form_submit_button("Send Voice", type="secondary")
                
                # Process file upload
                if voice_submit and audio_file:
                    with st.spinner("🎤 Processing voice input..."):
                        transcribed_text, bot_response, audio_response_path = self.process_voice_input(audio_file, tts_provider)
                        
                        if transcribed_text and bot_response:
                            # Add messages to chat
                            st.session_state.messages.append({"role": "user", "content": f"[Voice] {transcribed_text}"})
                            st.session_state.messages.append({"role": "assistant", "content": bot_response})
                            
                            # Store audio response path
                            if audio_response_path:
                                st.session_state.audio_response = audio_response_path
                            
                            st.session_state.voice_status = "✅ Voice processed successfully!"
                        else:
                            st.session_state.voice_status = f"❌ {transcribed_text}"
                        
                        st.rerun()
            
            # Clear chat button
            if st.button("🗑️ Clear Chat", type="secondary"):
                st.session_state.messages = []
                st.session_state.audio_response = None
                st.session_state.voice_status = None
                st.rerun()
            
            # Process text input
            if text_submit and text_input:
                # Add user message
                st.session_state.messages.append({"role": "user", "content": text_input})
                
                # Get bot response
                bot_response = self.process_text_input(text_input)
                if bot_response:
                    st.session_state.messages.append({"role": "assistant", "content": bot_response})
                
                st.rerun()
            
            # Display audio response if available
            if st.session_state.audio_response and os.path.exists(st.session_state.audio_response):
                st.markdown("### 🎵 Audio Response")
                with open(st.session_state.audio_response, "rb") as audio_file:
                    st.audio(audio_file.read(), format="audio/wav")
        
        with col2:
            st.markdown("### 🎯 What I can help with:")
            st.markdown("""
            <div class="feature-box">
                <ul>
                    <li>📱 Product recommendations</li>
                    <li>💰 Price comparisons</li>
                    <li>📦 Order tracking</li>
                    <li>🔄 Return policies</li>
                    <li>💳 Payment options</li>
                    <li>🚚 Shipping information</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 🎵 Voice Options:")
            st.markdown("""
            <div class="feature-box">
                <ul>
                    <li><strong>ElevenLabs:</strong> More natural, human-like voice</li>
                    <li><strong>gTTS (Google):</strong> Clear, reliable voice</li>
                    <li>Switch between them anytime!</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 💡 Quick Tips:")
            st.markdown("""
            <div class="feature-box">
                <ul>
                    <li>🎤 Use voice for hands-free shopping</li>
                    <li>💬 Type for detailed questions</li>
                    <li>🔍 Be specific about what you're looking for</li>
                    <li>❓ Ask follow-up questions</li>
                    <li>📚 Reference previous conversations</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 💭 Try asking:")
            st.markdown("""
            <div class="feature-box">
                <ul>
                    <li>"Show me smartphones under $1000"</li>
                    <li>"What's your return policy?"</li>
                    <li>"I need a laptop for gaming"</li>
                    <li>"How long does shipping take?"</li>
                    <li>"Remember when I ordered that laptop?"</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Voice troubleshooting
            st.markdown("### 🔧 Voice Troubleshooting:")
            st.markdown("""
            <div class="feature-box">
                <ul>
                    <li>🎤 Speak clearly and avoid background noise</li>
                    <li>📁 Use WAV, MP3, or M4A files</li>
                    <li>🔊 Check your microphone permissions</li>
                    <li>🌐 Ensure stable internet connection</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Database statistics
            try:
                stats = self.chatbot.db.get_conversation_statistics()
                st.markdown("### 📊 Conversation Stats:")
                st.markdown(f"""
                <div class="feature-box">
                    <ul>
                        <li>💬 Total conversations: {stats['total_conversations']}</li>
                        <li>📝 Total messages: {stats['total_messages']}</li>
                        <li>🆕 Recent conversations: {stats['recent_conversations']}</li>
                        <li>📈 Avg messages/conv: {stats['average_messages_per_conversation']}</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.warning("Could not load conversation statistics")
        
        # Welcome message (only show if no messages)
        if not st.session_state.messages:
            st.markdown("""
            <div class="chat-message bot-message">
                <strong>Alex:</strong> Hi there! 👋 I'm Alex, your friendly shopping assistant at ShopSmart. 
                I'm here to help you find the perfect products, answer questions about orders, or assist 
                with anything else you need. What can I help you with today?
                
                <br><br><strong>💡 Tip:</strong> I remember our previous conversations, so feel free to reference 
                past orders or questions!
            </div>
            """, unsafe_allow_html=True)

def main():
    """Main function to run the app"""
    app = load_app()
    app.initialize_session_state()
    app.create_interface()

if __name__ == "__main__":
    main() 