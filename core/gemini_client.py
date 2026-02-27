# core/gemini_client.py

import google.generativeai as genai
import os
from dotenv import load_dotenv
from config import MODEL_NAME, TEMPERATURE, MAX_OUTPUT_TOKENS

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    MODEL_NAME,
    generation_config={
        "temperature": TEMPERATURE,
        "max_output_tokens": MAX_OUTPUT_TOKENS,
    }
)
print("API KEY:", api_key)
def generate_response(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"