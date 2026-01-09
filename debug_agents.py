from src.agents.auditor import Auditor
from src.agents.fixer import Fixer
from src.agents.judge import Judge

# 1. Initialisation des classes (L'orchestrateur crée les objets)
auditeur = Auditor()
reparateur = Fixer()
juge = Judge()

# 2. Code de test (le "Patient")
code_sale = "def salut():\n    print(variable_inexistante)"

print("--- TEST AUDITEUR (Classe) ---")
# On appelle la méthode .run() de l'objet
rapport = auditeur.run(code_sale)
print(f"L'Auditeur dit : \n{rapport}\n")

print("--- TEST FIXER (Classe) ---")
code_propre = reparateur.run(code_sale, rapport)
print(f"Le Fixer propose : \n{code_propre}\n")

print("--- TEST JUDGE (Classe) ---")
verdict = juge.run(code_sale, code_propre)
print(f"Le Juge décide : \n{verdict}")