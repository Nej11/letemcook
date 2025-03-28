import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

try:
    models = genai.list_models()
    print("✅ Available Models:", [m.name for m in models])
except Exception as e:
    print("❌ API Key Issue:", str(e))
