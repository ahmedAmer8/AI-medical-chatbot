# 🩺 AI-Doctor: Medical Image Chatbot

![Banner](https://placehold.co/1200x300?text=AI+Doctor+Medical+Chatbot)

AI-Doctor is an intelligent chatbot that allows users to upload medical images (like skin conditions, scans, etc.) and ask health-related questions. It uses cutting-edge multimodal models (like LLaMA) via Groq API to interpret images and generate medically-relevant responses.

✅ Now available live on **Hugging Face Spaces**!  
👉 [Try it Online](https://huggingface.co/spaces/Ahmed-Amer/ai-doctor-medical-chatbot)

---

## 📷 Example

![Chat Example](./demo.png)

---

## 🚀 Features

- 🖼️ Upload medical images (e.g. skin, x-ray, MRI)
- 💬 Ask contextual questions about the image
- 🧠 Choose from multiple Groq-hosted LLaMA models
- 🔑 Use your own Groq API key or default one
- 💬 Modern chat interface (like WhatsApp)
- 🧾 Export conversation history as a report
- 🛠️ Easily deployable locally or on Hugging Face

---

## 🧠 Supported Models

All models are queried via the [Groq OpenAI-compatible API](https://groq.com):

- `meta-llama/llama-4-scout-17b-16e-instruct`
- `meta-llama/llama-3-8b-instruct`
- `meta-llama/llama-3-70b-instruct`

---

## 📁 File Structure

```bash
.
├── app.py                 # Main Gradio app with chat UI
├── main.py                # CLI image test runner
├── requirements.txt       # All Python dependencies
├── .env                   # For GROQ_API_KEY
├── README.md              # This documentation
```

---

## 💻 Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ahmedAmer8/ai-doctor-chatbot.git
cd ai-doctor-chatbot
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Add Your API Key

Create a `.env` file and add:

```
GROQ_API_KEY=your_default_key_here
```

> Note: Users can also input their own API key via the UI.

---

## ▶️ Run the App Locally

```bash
python app.py
```

Visit: [http://localhost:5000](http://localhost:5000)

---

## 🌐 Deployment on Hugging Face

To deploy on [Hugging Face Spaces](https://huggingface.co/spaces):

1. Upload `app.py`, `requirements.txt`, `.env` (optional)
2. Set your **Space type** to `Gradio`
3. Add secret `GROQ_API_KEY` via Space settings

Done! Your chatbot is now live.

---

## 📤 Exporting Reports

Click the **📥 Download Chat** button to get a full `.txt` file of the conversation, with both questions and answers.

Example:
```txt
User: What is that in the picture?
Doctor: The image shows signs of dandruff on the patient's scalp...
```

---

## 🎯 Tips for Best Results

| Tip | Reason |
|-----|--------|
| Upload clear, relevant images | Improves image understanding |
| Ask specific medical questions | Results are more actionable |
| Use consistent model | Prevents variation across answers |

---

## 🧪 Test via Script

You can run the model via CLI using `main.py`:

```bash
python main.py
```

Set your `image_path` and `query` in the file.

---

## 📚 Requirements

```txt
gradio
requests
Pillow
python-dotenv
```

Install with:

```bash
pip install -r requirements.txt
```

---

## 🛡️ License

MIT License — open for academic and commercial use.

---

## 🤝 Credits

- Groq API for blazing-fast model inference
- Meta AI for LLaMA models
- Gradio team for the frontend framework

---

## 📬 Contact

Email: ahmed.mohammad.amer@gmail.com  
GitHub: [@Ahmed-Amer](https://github.com/ahmedAmer8)

