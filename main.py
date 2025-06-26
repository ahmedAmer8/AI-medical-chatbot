import base64
import requests
import io
import mimetypes
from PIL import Image
from dotenv import load_dotenv
import os
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in the .env file")

def process_image(image_path, query):
    try:
        with open(image_path, "rb") as image_file:
            image_content = image_file.read()

        img = Image.open(io.BytesIO(image_content))
        img.verify()

        mime_type, _ = mimetypes.guess_type(image_path)
        if not mime_type:
            mime_type = "image/jpeg"

        encoded_image = base64.b64encode(image_content).decode("utf-8")
        image_data_url = f"data:{mime_type};base64,{encoded_image}"

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": query},
                    {"type": "image_url", "image_url": {"url": image_data_url}}
                ]
            }
        ]

        payload = {
            "model": MODEL_NAME,
            "messages": messages,
            "max_tokens": 1000
        }

        logger.info(f"Sending request:\n{json.dumps(payload, indent=2)[:1000]}...")

        response = requests.post(
            GROQ_API_URL,
            json=payload,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            logger.error(f"API Error: {response.status_code} - {response.text}")
            return f"Error: {response.status_code}"

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return f"Unexpected error: {str(e)}"

if __name__ == "__main__":
    image_path = "test1.png"
    query = "What are the anomalies in this scan?"
    result = process_image(image_path, query)
    print(result)
