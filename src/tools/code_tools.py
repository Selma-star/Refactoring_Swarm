import os
import subprocess

def write_file_safely(target_dir, filename, content):
    """
    Writes a file to the disk, but ONLY if it is inside the target_dir.
    This prevents the LLM from overwriting system files.
    """
    # 1. Security: Reject absolute paths (e.g. C:\Windows\...)
    if os.path.isabs(filename):
        raise PermissionError("Security Alert: Absolute paths are not allowed.")

    # 2. Construct the full path
    full_path = os.path.join(target_dir, filename)

    # 3. Normalize paths (resolve .. and .)
    # This converts 'target/../secret.txt' to 'secret.txt' (or absolute equivalent)
    norm_target = os.path.normpath(os.path.abspath(target_dir))
    norm_full = os.path.normpath(os.path.abspath(full_path))

    # 4. Check if the requested file is strictly inside the target folder
    if not norm_full.startswith(norm_target):
        raise PermissionError(f"Security Alert: Attempt to write outside sandbox. Target: {norm_target}, Requested: {norm_full}")

    # 5. Write the file
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return f"Successfully wrote {filename}"

def run_pytest(target_dir):
    """
    Runs pytest in the target directory and returns the output.
    """
    try:
        # -v for verbose output
        result = subprocess.run(['pytest', target_dir, '-v'], capture_output=True, text=True, timeout=30)
        output = result.stdout + result.stderr
        return output
    except FileNotFoundError:
        return "Error: pytest command not found. Make sure it is installed."
    except subprocess.TimeoutExpired:
        return "Error: Tests timed out."

def read_file(target_dir, filename):
    """
    Reads a single file from the target directory.
    """
    full_path = os.path.join(target_dir, filename)
    norm_target = os.path.normpath(os.path.abspath(target_dir))
    norm_full = os.path.normpath(os.path.abspath(full_path))

    # Security check
    if not norm_full.startswith(norm_target):
        raise PermissionError(f"Security Alert: Attempt to read outside sandbox: {full_path}")

    with open(full_path, 'r', encoding='utf-8') as f:
        return f.read()

def run_pylint(target_dir):
    """
    Runs pylint on the target directory and returns the raw output string.
    """
    try:
        # We run pylint on the directory. 
        # --output-format=text ensures we get the standard readable output.
        # --disable=C,R is optional, but let's run full pylint for strict checking unless needed.
        result = subprocess.run(['pylint', target_dir, '--output-format=text'], capture_output=True, text=True, timeout=30)
        output = result.stdout + result.stderr
        return output
    except FileNotFoundError:
        return "Error: pylint command not found. Make sure it is installed."
    except subprocess.TimeoutExpired:
        return "Error: Pylint timed out."