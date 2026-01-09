import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def run_judge(original_code, fixed_code):
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)
    
    # Lit le prompt du juge
    prompt_path = os.path.join("src", "prompts", "judge_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        instructions = f.read()

    model = genai.GenerativeModel('gemini-3-flash-preview')
    full_input = f"{instructions}\n\nAVANT:\n{original_code}\n\nAPRÈS:\n{fixed_code}"
    response = model.generate_content(full_input)
    return response.text