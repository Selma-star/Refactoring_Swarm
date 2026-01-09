import subprocess
import sys

def run_pytest(file_path):
    """Runs Pytest to ensure the code logic is correct."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", file_path],
            capture_output=True, 
            text=True
        )
        return result.stdout
    except Exception as e:
        return f"Pytest execution failed: {str(e)}"