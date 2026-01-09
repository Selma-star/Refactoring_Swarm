import os
from src.agents.auditor import Auditor
from src.agents.fixer import Fixer
from src.agents.judge import Judge

class Orchestrator:
    def __init__(self):
        # On initialise tes agents (Personne 3)
        self.auditor = Auditor()
        self.fixer = Fixer()
        self.judge = Judge()

    def process_file(self, file_path):
        # 1. Lecture du fichier buggé (Personne 2)
        with open(file_path, "r", encoding="utf-8") as f:
            original_code = f.read()

        print(f"--- Analyse de {file_path} ---")

        # 2. Appel de tes agents
        report = self.auditor.run(original_code)
        fixed_code = self.fixer.run(original_code, report)
        verdict = self.judge.run(original_code, fixed_code)

        # 3. Vérification du verdict
        if "PASS" in verdict.upper():
            self._save_changes(file_path, fixed_code)
            return True, verdict
        else:
            return False, verdict

    def _save_changes(self, file_path, new_code):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_code)
        print(f"✅ Code corrigé appliqué à {file_path}")