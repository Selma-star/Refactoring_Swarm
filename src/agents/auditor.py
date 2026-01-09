import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def run_auditor(code_to_analyze):
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)
    
    # Lit le prompt de l'auditeur
    prompt_path = os.path.join("src", "prompts", "auditor_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        instructions = f.read()

    model = genai.GenerativeModel('gemini-3-flash-preview')
    response = model.generate_content(f"{instructions}\n\nCode à analyser :\n{code_to_analyze}")
    return response.text