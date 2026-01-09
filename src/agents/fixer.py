import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class Fixer:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-3-flash-preview')
        
        prompt_path = os.path.join("src", "prompts", "fixer_prompt.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.instructions = f.read()

    def run(self, original_code, audit_report):
        full_input = (
            f"{self.instructions}\n\n"
            f"CODE ORIGINAL:\n{original_code}\n\n"
            f"RAPPORT AUDIT:\n{audit_report}"
        )
        response = self.model.generate_content(full_input)
        return response.text