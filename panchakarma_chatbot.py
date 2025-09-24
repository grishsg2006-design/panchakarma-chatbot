import google.generativeai as genai
import streamlit as st

# --------------------------
# Configure Gemini API Key
# --------------------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --------------------------
# Gemini Response Generator
# --------------------------
def get_gemini_response(user_message, therapy_type=None):
    """
    Generate response using Gemini AI.
    Fully AI-based; does NOT rely on any knowledge base.
    """
    # System prompt guiding the AI
    system_prompt = """
You are an empathetic Ayurvedic assistant specializing in Panchakarma and general Ayurveda.
Answer the user's questions fully, clearly, and accurately.
- Use bullet points where appropriate.
- Focus on the therapy type if provided.
- End with: "This is general guidance based on traditional Ayurveda—consult your qualified practitioner for personalized advice."
"""

    # Append therapy type if given
    if therapy_type:
        system_prompt += f"\n\nFocus on therapy type: {therapy_type}"

    # Combine system prompt with user message
    prompt = f"{system_prompt}\n\nUser question: {user_message}"

    try:
        gemini_model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = gemini_model.generate_content([
            {"role": "user", "parts": prompt}
        ])
        return response.text.strip()
    except Exception as e:
        return f"Error generating response: {str(e)}. Check your Gemini API key and internet connection."

# --------------------------
# Optional Console Mode
# --------------------------
def run_console_chatbot():
    print("=== Panchakarma Chatbot (Gemini AI Console Mode) ===")
    therapy_type = input("Enter therapy type (optional, e.g., Virechana): ").strip()
    print(f"Therapy set to: {therapy_type or 'General'}\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Thank you! Stay healthy.")
            break
        if not user_input:
            continue
        print("\nBot: ", end="")
        response = get_gemini_response(user_input, therapy_type)
        print(response)
        print("-" * 50)

if __name__ == "__main__":
    run_console_chatbot()
