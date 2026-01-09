from src.orchestrator import Orchestrator

def main():
    # Initialisation de l'orchestrateur
    swarm = Orchestrator()
    
    # Fichier cible
    target = "test_dataset/buggy1.py"
    
    print("🚀 Lancement du Swarm de Refactoring...")
    
    success, message = swarm.process_file(target)
    
    if success:
        print("✨ Mission réussie : Le code a été remplacé.")
    else:
        print(f"⚠️ Échec du remplacement. Raison : {message}")

if __name__ == "__main__":
    main()