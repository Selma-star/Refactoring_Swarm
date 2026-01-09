import os
from dotenv import load_dotenv
import google.generativeai as genai

# 1. On charge le .env
load_dotenv(override=True)
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Erreur : Clé manquante.")
else:
    genai.configure(api_key=api_key)
    
    # En 2026, la version stable pour l'API est celle-ci :
    model = genai.GenerativeModel('gemini-3-flash-preview') 

    try:
        # Test de connexion
        response = model.generate_content("Dis : Connexion établie")
        print(f"✅ RÉPONSE : {response.text}")
    except Exception as e:
        print(f"❌ Erreur : {e}")