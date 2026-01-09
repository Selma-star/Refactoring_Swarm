#!/usr/bin/env python3
"""
MAIN ENTRY POINT - This is what the AutoCorrect Bot will run
Command: python main.py --target_dir "./sandbox/dataset_inconnu"
"""

import argparse
import os
import sys
from pathlib import Path

# This lets Python find our code in the src/ folder
sys.path.append(str(Path(__file__).parent))

# Import our orchestrator
try:
    from src.orchestrator import RefactoringOrchestrator
except ImportError:
    print("❌ ERROR: Cannot import orchestrator. Make sure src/orchestrator.py exists!")
    sys.exit(1)


def validate_directory(path: str) -> bool:
    """Check if directory exists and is readable."""
    path_obj = Path(path)
    
    if not path_obj.exists():
        print(f"❌ Error: Directory '{path}' does not exist.")
        return False
    
    if not path_obj.is_dir():
        print(f"❌ Error: '{path}' is not a directory.")
        return False
    
    return True


def main():
    """This function runs when someone starts the program."""
    
    # STEP 1: Handle command line arguments
    parser = argparse.ArgumentParser(
        description="Refactoring Swarm - Fixes buggy Python code automatically",
        epilog="""
Examples:
  For testing:    python main.py --target_dir "./test_dataset"
  For AutoCorrect: python main.py --target_dir "./sandbox/dataset_inconnu"
        """
    )
    
    # This is REQUIRED - the AutoCorrect Bot will provide it
    parser.add_argument(
        "--target_dir",
        type=str,
        required=True,
        help="Folder containing Python files to fix"
    )
    
    # Optional: for debugging
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed progress"
    )
    
    # Get the arguments from command line
    args = parser.parse_args()
    
    # STEP 2: Validate the directory
    if not validate_directory(args.target_dir):
        sys.exit(1)
    
    # STEP 3: Show startup message
    print("=" * 60)
    print("🔄 REFACTORING SWARM - Starting...")
    print(f"📁 Target: {args.target_dir}")
    print("=" * 60)
    
    # STEP 4: Create and run the orchestrator
    try:
        orchestrator = RefactoringOrchestrator(
            target_dir=args.target_dir,
            verbose=args.verbose
        )
        
        success = orchestrator.run()
        
        # STEP 5: Show result
        if success:
            print("\n" + "=" * 60)
            print("✅ REFACTORING COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            sys.exit(0)  # 0 means success
        else:
            print("\n" + "=" * 60)
            print("❌ Refactoring failed or incomplete.")
            print("=" * 60)
            sys.exit(1)  # 1 means error
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Process interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


# This makes the program run when you type "python main.py"
if __name__ == "__main__":
    main()