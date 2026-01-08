# working_test.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)

# Use the model that works
model = genai.GenerativeModel('gemini-flash-latest')
response = model.generate_content("Say hello in one word")
print(f"✅ Works! Response: {response.text}")