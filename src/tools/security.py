import os

def validate_path(file_path):
    """Ensures the agent is only working inside the 'sandbox' or 'test_dataset' folders."""
    abs_path = os.path.abspath(file_path)
    current_dir = os.getcwd()
    
    # Restrict access to specific project subfolders only
    allowed_dirs = [
        os.path.join(current_dir, "sandbox"),
        os.path.join(current_dir, "test_dataset")
    ]
    
    return any(abs_path.startswith(d) for d in allowed_dirs)