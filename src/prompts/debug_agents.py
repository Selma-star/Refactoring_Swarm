from src.agents.auditor import run_auditor
from src.agents.fixer import run_fixer
from src.agents.judge import run_judge

# 1. Un code simple avec une erreur pour le test
code_sale = "def salut():\n    print(variable_inexistante)"

print("--- TEST AUDITEUR ---")
rapport = run_auditor(code_sale)
print(f"L'Auditeur dit : \n{rapport}\n")

print("--- TEST FIXER ---")
code_propre = run_fixer(code_sale, rapport)
print(f"Le Fixer propose : \n{code_propre}\n")

print("--- TEST JUDGE ---")
verdict = run_judge(code_sale, code_propre)
print(f"Le Juge décide : \n{verdict}")