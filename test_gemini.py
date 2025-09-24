import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# List available models
models = genai.list_models()
print("Available Gemini Models:")
for m in models:
    if "generateContent" in m.supported_generation_methods:
        print("-", m.name)

# Simple test
model = genai.GenerativeModel("models/gemini-1.5-flash")
response = model.generate_content("Hello Gemini! Give me one Panchakarma tip.")
print("\nSample Response:\n", response.text)
