# Ecokart E-commerce Voice Assistant (Gradio/Hugging Face Spaces)

## 🚀 Deploy on Hugging Face Spaces (with Microphone Support)

### 1. Setup
- Clone this repo or upload your code to a new Hugging Face Space.
- Make sure your `requirements.txt` is present and includes all dependencies.
- Set your environment variables (API keys) in the Hugging Face Space settings:
  - `GROQ_API_KEY`
  - `ELEVEN_API_KEY`

### 2. Usage
- The app will launch with a Gradio interface.
- You can use the microphone button to record your question, or type your question in the text box.
- The bot will respond with both text and voice.

### 3. Notes
- All product info is grounded in your `data.txt` catalog.
- If a product is in the catalog, the bot will always use the catalog price and description.
- All errors are logged to `app.log`.

### 4. Troubleshooting
- If you see errors about missing API keys, set them in the Space's Secrets.
- If audio does not play, check your browser permissions for microphone and audio.

---

For more help, see the Hugging Face Spaces documentation: https://huggingface.co/docs/spaces 