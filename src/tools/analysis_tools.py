import subprocess
import sys

def run_pylint(file_path):
    """Runs Pylint using the explicit venv executable."""
    try:
        # sys.executable forces the use of the active (venv) python
        result = subprocess.run(
            [sys.executable, "-m", "pylint", "--exit-zero", file_path],
            capture_output=True, 
            text=True,
            shell=False
        )
        
        # We take stdout if it exists, otherwise stderr
        output = result.stdout.strip() or result.stderr.strip()
        return output if output else "Pylint produced no output."
        
    except Exception as e:
        return f"Tool Execution Error: {str(e)}"