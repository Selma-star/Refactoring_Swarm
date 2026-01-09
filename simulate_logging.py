# simulate_logs.py


import os
from src.utils.logger import log_experiment, ActionType

# 1️⃣ Chemin vers le dossier des fichiers buggés
TEST_DIR = "test_dataset"
test_files = [f for f in os.listdir(TEST_DIR) if f.endswith(".py")]

# 2️⃣ Boucle sur chaque fichier pour simuler les actions
for file_name in test_files:
    file_path = os.path.join(TEST_DIR, file_name)

    # --- Auditor Simulation ---
    log_experiment(
        agent_name="Auditor",
        model_used="gemini-1.5-flash",
        action=ActionType.ANALYSIS,
        details={
            "input_prompt": f"Analyse le fichier {file_name}",
            "output_response": f"Bug trouvé dans {file_name} : variable non définie"
        },
        status="SUCCESS"
    )

    # --- Fixer Simulation ---
    log_experiment(
        agent_name="Fixer",
        model_used="gemini-1.5-flash",
        action=ActionType.FIX,
        details={
            "input_prompt": f"Corrige le bug dans {file_name}",
            "output_response": f"Ajout de la définition de variable manquante dans {file_name}"
        },
        status="SUCCESS"
    )

    # --- Judge Simulation ---
    log_experiment(
        agent_name="Judge",
        model_used="pytest",
        action=ActionType.DEBUG,
        details={
            "input_prompt": f"Test du fichier corrigé {file_name}",
            "output_response": "Tous les tests passent"
        },
        status="SUCCESS"
    )

print("✅ Simulation complete. Logs are saved in logs/experiment_data.json")
