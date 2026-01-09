import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class Auditor:
    def __init__(self):
        # Configuration de l'API
        api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-3-flash-preview')
        
        # Chargement du prompt
        prompt_path = os.path.join("src", "prompts", "auditor_prompt.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.instructions = f.read()

    def run(self, code_to_analyze):
        full_input = f"{self.instructions}\n\nCode à analyser :\n{code_to_analyze}"
        response = self.model.generate_content(full_input)
        return response.text