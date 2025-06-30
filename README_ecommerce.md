# 🛍️ ShopSmart E-commerce Voice Assistant

A conversational AI assistant for e-commerce that can chat like a real human! Meet Alex, your friendly shopping assistant who can help you find products, answer questions about orders, and provide a natural shopping experience through both voice and text interactions.

## ✨ Features

- **🎤 Voice Interaction**: Natural speech-to-speech conversation
- **💬 Text Chat**: Traditional text-based chat interface
- **🤖 Human-like Responses**: Conversational AI that feels like talking to a real person
- **📱 Product Knowledge**: Built-in product database with recommendations
- **🛒 E-commerce Expertise**: Order tracking, returns, shipping, and payment information
- **🌐 Web Interface**: Beautiful Gradio web app for easy access
- **🎯 Context Awareness**: Remembers conversation history for better interactions

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed on your system
2. **FFmpeg** and **PortAudio** for audio processing
3. **API Keys** for Groq and ElevenLabs

### Installation

1. **Clone or download the project files**

2. **Install FFmpeg and PortAudio** (see platform-specific instructions below)

3. **Set up Python environment**:
   ```bash
   # Using pip and venv
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ELEVEN_API_KEY=your_elevenlabs_api_key_here
   ```

### Platform-Specific Setup

#### Windows
1. **FFmpeg**: Download from [FFmpeg Downloads](https://ffmpeg.org/download.html)
   - Extract to `C:\ffmpeg`
   - Add `C:\ffmpeg\bin` to your system PATH

2. **PortAudio**: Download from [PortAudio Downloads](http://www.portaudio.com/download.html)

#### macOS
```bash
brew install ffmpeg portaudio
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg portaudio19-dev
```

## 🎯 Usage

### Option 1: Voice Assistant (Command Line)
Run the voice assistant for hands-free shopping:
```bash
python ecommerce_voice_assistant.py
```

**Features:**
- 🎤 Voice input and output
- 🔄 Continuous conversation loop
- 👋 Natural greetings and farewells
- 🎯 Context-aware responses

### Option 2: Web Interface (Gradio)
Launch the beautiful web interface:
```bash
python ecommerce_gradio_app.py
```

**Features:**
- 💬 Text and voice input options
- 🎨 Modern, responsive UI
- 📱 Mobile-friendly design
- 🔄 Real-time conversation history

### Option 3: Chatbot Brain Only
Test the core chatbot logic:
```bash
python ecommerce_brain.py
```

## 💬 Sample Conversations

### Product Inquiries
```
Customer: "I'm looking for a new smartphone under $1000"
Alex: "Great choice! I found some excellent options for you. The iPhone 15 Pro at $999 has an A17 Pro chip and 48MP camera, while the Samsung Galaxy S24 at $899 features a Snapdragon 8 Gen 3 and 200MP camera. Both are fantastic choices! What's most important to you - camera quality, performance, or battery life? 📱"
```

### Order Support
```
Customer: "What's your return policy?"
Alex: "We want you to be completely happy with your purchase! Our return policy is pretty straightforward - you have 30 days from delivery to return most items in their original condition. Electronics have a 14-day return window. Just make sure the item is unused and in its original packaging. Need help with a specific return? 😊"
```

### General Questions
```
Customer: "How long does shipping take?"
Alex: "Shipping times depend on your location and the shipping method you choose! Standard shipping usually takes 3-5 business days, while express shipping gets your order to you in 1-2 business days. We also offer same-day delivery in select areas. Where are you located? I can give you a more specific estimate! 🚚"
```

## 🛠️ Customization

### Adding Products
Edit the `products` dictionary in `ecommerce_brain.py`:
```python
self.products = {
    "your_category": {
        "your_subcategory": [
            {
                "name": "Product Name",
                "price": 99.99,
                "features": ["Feature 1", "Feature 2", "Feature 3"]
            }
        ]
    }
}
```

### Changing Voice
Modify the voice settings in `ecommerce_voice_assistant.py`:
```python
self.voice_name = "Your_Preferred_Voice"  # ElevenLabs voice name
```

### Customizing Personality
Update the `system_prompt` in `ecommerce_brain.py` to change Alex's personality and responses.

## 🔧 API Keys Required

### Groq API Key
1. Sign up at [Groq Console](https://console.groq.com/)
2. Create an API key
3. Add to `.env` file: `GROQ_API_KEY=your_key_here`

### ElevenLabs API Key
1. Sign up at [ElevenLabs](https://elevenlabs.io/)
2. Get your API key from the profile section
3. Add to `.env` file: `ELEVEN_API_KEY=your_key_here`

## 📁 Project Structure

```
├── ecommerce_brain.py           # Core chatbot logic and product database
├── ecommerce_voice_assistant.py # Voice interaction system
├── ecommerce_gradio_app.py      # Web interface
├── requirements.txt             # Python dependencies
├── README_ecommerce.md          # This file
└── .env                        # Environment variables (create this)
```

## 🎨 Features in Detail

### Human-like Conversation
- **Natural Language**: Responses feel like talking to a real person
- **Emojis and Personality**: Friendly, engaging communication style
- **Context Awareness**: Remembers previous conversation topics
- **Follow-up Questions**: Asks clarifying questions to better assist

### Product Intelligence
- **Smart Search**: Finds products based on descriptions and categories
- **Price Filtering**: Can filter by price ranges
- **Feature Matching**: Suggests products based on specific needs
- **Recommendations**: Offers related products and alternatives

### E-commerce Expertise
- **Order Management**: Help with tracking, status, and modifications
- **Return Policies**: Clear information about returns and refunds
- **Shipping Options**: Multiple shipping methods and timeframes
- **Payment Security**: Information about payment methods and security

## 🚀 Future Enhancements

- [ ] **Database Integration**: Connect to real product databases
- [ ] **Order Processing**: Actual order placement capabilities
- [ ] **User Accounts**: Personalized shopping experiences
- [ ] **Multi-language Support**: Support for multiple languages
- [ ] **Mobile App**: Native mobile application
- [ ] **Analytics**: Conversation analytics and insights

## 🤝 Contributing

Feel free to contribute to this project! Some areas for improvement:
- Add more product categories
- Enhance conversation flow
- Improve voice quality
- Add more e-commerce features

## 📞 Support

If you encounter any issues:
1. Check that all dependencies are installed
2. Verify your API keys are correct
3. Ensure FFmpeg and PortAudio are properly installed
4. Check the console for error messages

## 🎉 Enjoy Shopping!

Start your conversation with Alex and experience the future of e-commerce customer service! 🛍️✨ 