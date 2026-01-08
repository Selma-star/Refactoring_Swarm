import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load the key from your .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Error: No API Key found in .env file!")
else:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-3-flash-preview')
        response = model.generate_content("Say 'The Swarm is ready' if you can hear me.")
        print(f"✅ Success! AI Response: {response.text}")
    except Exception as e:
        print(f"❌ API Test Failed: {e}")