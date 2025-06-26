import gradio as gr
import base64
import requests
import io
from PIL import Image
import os
from dotenv import load_dotenv
import logging
from datetime import datetime
import tempfile

# Load environment and logging
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_API_KEY = os.getenv("GROQ_API_KEY")
AVAILABLE_MODELS = [
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "meta-llama/llama-3-8b-instruct",
    "meta-llama/llama-3-70b-instruct"
]

# Format messages for exporting report
def format_chat_as_text(chat):
    return "\n\n".join([f"User: {u}\nDoctor: {a}" for u, a in chat])

# Save chat to file for download
def download_report(chat):
    text = format_chat_as_text(chat)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(tempfile.gettempdir(), f"chat_report_{timestamp}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)
    return file_path

# Main logic
def handle_chat(user_input, image, model, user_api_key, history):
    api_key = user_api_key.strip() if user_api_key.strip() else DEFAULT_API_KEY
    if not api_key:
        return history + [[user_input, "❌ No API key provided."]], ""

    try:
        # Image prep
        if image:
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            image_bytes = buffered.getvalue()
            encoded_image = base64.b64encode(image_bytes).decode("utf-8")
            Image.open(io.BytesIO(image_bytes)).verify()
            image_url = f"data:image/jpeg;base64,{encoded_image}"
        else:
            image_url = None

        # Build message history
        messages = []
        for turn in history:
            if turn[0]:
                messages.append({"role": "user", "content": [{"type": "text", "text": turn[0]}]})
            if turn[1]:
                messages.append({"role": "assistant", "content": turn[1]})  # plain string only

        # Add current user input with optional image
        content = [{"type": "text", "text": user_input}]
        if image_url:
            content.append({"type": "image_url", "image_url": {"url": image_url}})
        messages.append({"role": "user", "content": content})

        # Prepare payload
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": 1000
        }

        response = requests.post(
            GROQ_API_URL,
            json=payload,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            answer = result["choices"][0]["message"]["content"]
            history.append([user_input, answer])
            return history, ""
        else:
            logger.error(f"API Error: {response.status_code} - {response.text}")
            return history + [[user_input, f"❌ API Error: {response.status_code}"]], ""

    except Exception as e:
        logger.error(f"Exception: {e}")
        return history + [[user_input, f"❌ Unexpected error: {str(e)}"]], ""

# UI
with gr.Blocks(css=".gr-chatbot .message.user {background-color:#dcf8c6 !important;} .gr-chatbot .message.bot {background-color:#ececec !important;} .gr-chatbot {font-size: 1.1rem;}") as demo:
    gr.Markdown("# 🩺 AI Doctor: Medical Image Chatbot")

    with gr.Row():
        with gr.Column(scale=1):
            image_input = gr.Image(type="pil", label="📤 Optional: Upload Image")
            model_choice = gr.Dropdown(choices=AVAILABLE_MODELS, value=AVAILABLE_MODELS[0], label="🧠 Choose Model")
            api_key_input = gr.Textbox(label="🔐 Your API Key (optional)", type="password", placeholder="Leave blank to use default")
            download_btn = gr.Button("📥 Download Chat")

        with gr.Column(scale=2):
            chatbot = gr.Chatbot(label="👨‍⚕️ Doctor Chat", height=500)
            chat_input = gr.Textbox(show_label=False, placeholder="Type your medical question here and press Enter...")
            hidden_report_text = gr.Textbox(visible=False)

    # Chat input handling
    chat_input.submit(
        fn=handle_chat,
        inputs=[chat_input, image_input, model_choice, api_key_input, chatbot],
        outputs=[chatbot, hidden_report_text],
    ).then(lambda: "", None, chat_input)  # clear input after submit

    # Download
    download_btn.click(fn=download_report, inputs=chatbot, outputs=gr.File())

# Run app
if __name__ == "__main__":
    demo.launch(server_port=5000)
