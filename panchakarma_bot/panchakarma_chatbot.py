import os
import faiss
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import streamlit as st

# --------------------------
# Configure Gemini API Key
# --------------------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --------------------------
# Load Knowledge Base
# --------------------------
def load_knowledge_base(file_path="panchakarma_precautions.txt"):
    """Load knowledge base from a text file."""
    global knowledge_base
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    knowledge_base = [section.strip() for section in content.split("\n\n") if section.strip()]
    return knowledge_base

knowledge_base = load_knowledge_base()

# --------------------------
# RAG Setup
# --------------------------
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(knowledge_base)
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings.astype('float32'))

def retrieve_relevant_info(query, k=2):
    """Retrieve top-k relevant sections from the knowledge base."""
    if not knowledge_base:
        return []
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding.astype('float32'), k)
    return [knowledge_base[i] for i in indices[0] if i < len(knowledge_base)]

# --------------------------
# Gemini Response Generator (Hybrid)
# --------------------------
def get_gemini_response(user_message, therapy_type=None):
    """
    Generate response using Gemini:
    - Use RAG if relevant info exists
    - Otherwise, rely on Gemini general knowledge
    """
    relevant_info = retrieve_relevant_info(user_message)
    
    if relevant_info:
        context = "\n\n".join(relevant_info)
        prompt = f"""
You are an empathetic Ayurvedic assistant specializing in Panchakarma.
Use the following context to answer the user's question accurately:

Context:
{context}

User question: {user_message}

Instructions:
- Summarize key points in bullet points if relevant.
- If therapy_type is given, focus on it.
- Be clear, concise, and supportive.
- If the question is outside the context, answer using your general Ayurvedic knowledge.
- End with: "This is general guidance based on Ayurveda—consult your practitioner for personalized advice."
"""
    else:
        # No relevant context found; rely entirely on Gemini
        prompt = f"""
You are an empathetic Ayurvedic assistant specializing in Panchakarma.
User question: {user_message}

Instructions:
- Answer using your general Ayurvedic knowledge.
- Summarize key points in bullet points if possible.
- If therapy_type is given, focus on it.
- End with: "This is general guidance based on Ayurveda—consult your practitioner for personalized advice."
"""

    if therapy_type:
        prompt += f"\n\nFocus on: {therapy_type}"

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
    print("=== Panchakarma Chatbot (Hybrid Gemini Console Mode) ===")
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
