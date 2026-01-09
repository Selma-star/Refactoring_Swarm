"""
Analyse le fichier logs/experiment_data.json et génère un rapport résumé
pour chaque agent et chaque fichier traité.
"""

import json
from collections import defaultdict

LOG_FILE = "logs/experiment_data.json"

# 1️⃣ Lecture des logs
try:
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"❌ Fichier {LOG_FILE} introuvable ! Assurez-vous que simulate_logs.py a été exécuté.")
    exit(1)
except json.JSONDecodeError:
    print(f"❌ Le fichier {LOG_FILE} est corrompu ou mal formé !")
    exit(1)

# 2️⃣ Préparer les compteurs
agent_stats = defaultdict(lambda: {"count": 0, "success": 0, "failure": 0})
file_stats = defaultdict(lambda: {"analyzed": 0, "fixed": 0, "tested": 0})

# 3️⃣ Parcourir chaque entrée de log
for entry in data:
    agent = entry.get("agent", "Unknown")
    status = entry.get("status", "UNKNOWN")
    action = entry.get("action", "UNKNOWN")
    details = entry.get("details", {})

    # Si details est une string (ex: System), on le convertit en dict vide
    if not isinstance(details, dict):
        details = {}

    # Statistiques par agent
    agent_stats[agent]["count"] += 1
    if status.upper() == "SUCCESS":
        agent_stats[agent]["success"] += 1
    elif status.upper() == "FAILURE":
        agent_stats[agent]["failure"] += 1

    # Statistiques par fichier (si input_prompt contient un nom de fichier)
    input_prompt = details.get("input_prompt", "")
    for word in input_prompt.split():
        if word.endswith(".py"):
            file_name = word
            if action == "CODE_ANALYSIS":
                file_stats[file_name]["analyzed"] += 1
            elif action == "FIX":
                file_stats[file_name]["fixed"] += 1
            elif action == "DEBUG":
                file_stats[file_name]["tested"] += 1

# 4️⃣ Affichage du rapport
print("\n===== RAPPORT PAR AGENT =====")
for agent, stats in agent_stats.items():
    print(f"{agent}: Total={stats['count']}, Success={stats['success']}, Failure={stats['failure']}")

print("\n===== RAPPORT PAR FICHIER =====")
if file_stats:
    for file, stats in file_stats.items():
        print(f"{file}: Analyzed={stats['analyzed']}, Fixed={stats['fixed']}, Tested={stats['tested']}")
else:
    print("Aucun fichier traité trouvé dans les logs.")

print("\n✅ Analyse terminée.")
