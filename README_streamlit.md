# ShopSmart E-commerce Voice Assistant - Streamlit Web Interface

## 🛍️ Overview

This is a modern, beautiful Streamlit web interface for the Ecokart E-commerce Voice Assistant. It provides an intuitive way to interact with Harvey Spectre, your AI shopping assistant, through both text and voice interactions.

## ✨ Features

### 💬 Text Chat
- Real-time text-based conversations with Harvey Spectre
- Natural language processing for product queries
- Context-aware responses
- Chat history management

### �� Voice Interaction
- Voice input support (upload audio files)
- Speech-to-text transcription
- Text-to-speech response generation
- Multiple voice providers (ElevenLabs, Google TTS)

### 🎨 Modern UI
- Beautiful gradient design
- Responsive layout
- Intuitive navigation
- Feature highlights and tips
- Sample questions for guidance

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- All dependencies installed (run `python setup.py`)
- API keys configured in `.env` file

### Running the App

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Streamlit app:**
   ```bash
   python -m streamlit run ecommerce_streamlit_app.py
   ```

3. **Open your browser:**
   The app will automatically open at `http://localhost:8501`

## 🎯 What Harvey Spectre Can Help With

- 📱 **Product Recommendations** - Find the perfect products for your needs
- 💰 **Price Comparisons** - Compare prices across different items
- 📦 **Order Tracking** - Get updates on your orders
- 🔄 **Return Policies** - Understand return and refund processes
- 💳 **Payment Options** - Learn about available payment methods
- 🚚 **Shipping Information** - Get shipping details and estimates

## 🎵 Voice Options

### ElevenLabs
- More natural, human-like voice
- Higher quality audio output
- Better emotional expression

### Google TTS (gTTS)
- Clear, reliable voice
- Fast processing
- Good for quick responses

## 💡 Usage Tips

1. **Text Chat:**
   - Type your questions in the text area
   - Be specific about what you're looking for
   - Ask follow-up questions for better recommendations

2. **Voice Input:**
   - Upload audio files (WAV, MP3, M4A)
   - Speak clearly for better transcription
   - Choose your preferred voice provider

3. **Getting Started:**
   - Try the sample questions provided
   - Use the feature highlights for guidance
   - Clear chat history when needed

## 🔧 Configuration

### Environment Variables
Create a `.env` file with your API keys:
```
GROQ_API_KEY=your_groq_api_key_here
ELEVEN_API_KEY=your_elevenlabs_api_key_here
```

### API Keys
- **Groq API Key:** Get from [Groq Console](https://console.groq.com/)
- **ElevenLabs API Key:** Get from [ElevenLabs](https://elevenlabs.io/)

## 🎨 Customization

### Styling
The app uses custom CSS for styling. You can modify the appearance by editing the CSS in the `st.markdown()` section.

### Features
- Add new product categories in `ecommerce_brain.py`
- Modify the system prompt for different personalities
- Add new voice providers in `ecommerce_voice_assistant.py`

## 🐛 Troubleshooting

### Getting Help
- Run `python setup.py` to check your configuration
- Check the console for error messages
- Verify all dependencies are installed

### Common Issues

1. **"streamlit command not found":**
   - Use `python -m streamlit run ecommerce_streamlit_app.py` instead
   - This is common on Windows when packages are installed in user directories

2. **Audio not playing:**
   - Check if FFmpeg is installed
   - Ensure audio files are in supported formats

3. **Voice transcription issues:**
   - Speak clearly and avoid background noise
   - Use supported audio formats (WAV, MP3, M4A)

4. **API errors:**
   - Verify API keys are correctly set in `.env`
   - Check internet connection
   - Ensure API quotas haven't been exceeded

## 📱 Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge

## 🔒 Security Notes

- API keys are stored locally in `.env` file
- No data is sent to external servers except for API calls
- Audio files are processed locally and not stored permanently

## 🚀 Deployment

### Local Development
```bash
python -m streamlit run ecommerce_streamlit_app.py
```

### Production Deployment
For production deployment, consider:
- Using Streamlit Cloud
- Setting up proper environment variables
- Implementing authentication if needed
- Using HTTPS for secure connections

## 📄 License

This project is part of the ShopSmart E-commerce Voice Assistant suite.

---

**Happy Shopping with Harvey Spectre! 🛍️✨** 