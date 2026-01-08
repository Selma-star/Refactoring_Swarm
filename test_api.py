import os
from dotenv import load_dotenv
import google.generativeai as genai

# 1. Charger le fichier .env
load_dotenv()

# 2. Récupérer la clé API
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Erreur : GEMINI_API_KEY non trouvée dans le fichier .env")
else:
    try:
        # 3. Configurer l'IA
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        # 4. Faire un test simple
        response = model.generate_content("Dis 'La connexion API fonctionne !' en français.")
        
        print("-" * 30)
        print("✅ SUCCÈS !")
        print(f"Réponse de l'IA : {response.text}")
        print("-" * 30)
        
    except Exception as e:
        print("❌ Une erreur est survenue lors de l'appel à l'API :")
        print(e)