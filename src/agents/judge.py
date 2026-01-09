import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class Judge:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-3-flash-preview')
        
        prompt_path = os.path.join("src", "prompts", "judge_prompt.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.instructions = f.read()

    def run(self, original_code, fixed_code):
        full_input = (
            f"{self.instructions}\n\n"
            f"AVANT:\n{original_code}\n\n"
            f"APRÈS:\n{fixed_code}"
        )
        response = self.model.generate_content(full_input)
        return response.text