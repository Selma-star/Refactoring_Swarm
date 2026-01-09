"""
ORCHESTRATOR - The conductor that coordinates all agents
"""

import os
import time
from pathlib import Path


class RefactoringOrchestrator:
    """Main controller that runs Auditor → Fixer → Judge in sequence."""
    
    def __init__(self, target_dir: str, verbose: bool = False):
        """
        Initialize the orchestrator.
        
        Args:
            target_dir: Folder with buggy Python files
            verbose: Show detailed progress messages
        """
        self.target_dir = Path(target_dir).resolve()
        self.verbose = verbose
        self.max_iterations = 10  # Safety: don't loop forever
        
        # We'll create these agents later
        self.auditor = None
        self.fixer = None
        self.judge = None
        
        # Track progress
        self.files_processed = []
        self.files_failed = []
    
    def _discover_files(self):
        """Find all Python files in the target folder."""
        if self.verbose:
            print("\n🔍 Scanning for Python files...")
        
        python_files = []
        
        # Check if target is a file instead of directory
        if self.target_dir.is_file() and self.target_dir.suffix == '.py':
            python_files.append(self.target_dir)
            if self.verbose:
                print(f"📄 Single file: {self.target_dir.name}")
        else:
            # Walk through directory
            for root, dirs, files in os.walk(self.target_dir):
                for file in files:
                    if file.endswith('.py'):
                        full_path = Path(root) / file
                        python_files.append(full_path)
        
        print(f"\n📄 Found {len(python_files)} Python file(s)")
        
        if python_files and self.verbose:
            for file in python_files[:5]:  # Show first 5
                print(f"   - {file.relative_to(self.target_dir)}")
            if len(python_files) > 5:
                print(f"   ... and {len(python_files) - 5} more")
        
        return python_files
    
    def _initialize_agents(self):
        """Create the three AI agents."""
        print("\n🤖 Initializing agents...")
        
        # These imports will work after your teammates create the agents
        try:
            from src.agents.auditor import AuditorAgent
            from src.agents.fixer import FixerAgent
            from src.agents.judge import JudgeAgent
            
            self.auditor = AuditorAgent(verbose=self.verbose)
            self.fixer = FixerAgent(verbose=self.verbose)
            self.judge = JudgeAgent(verbose=self.verbose)
            
            print("✅ Agents created successfully")
        except ImportError as e:
            print(f"❌ Cannot import agents: {e}")
            print("\n👉 YOUR TEAMMATES NEED TO CREATE THESE FILES:")
            print("   1. Person 3: Create src/agents/auditor.py")
            print("   2. Person 3: Create src/agents/fixer.py")
            print("   3. Person 3: Create src/agents/judge.py")
            raise
    
    def _process_single_file(self, file_path):
        """Fix one Python file using the 3 agents."""
        print(f"\n{'='*50}")
        print(f"📄 Processing: {file_path.name}")
        print(f"{'='*50}")
        
        try:
            # STEP 1: AUDIT - Find problems
            print("1. 🔍 Auditor analyzing...")
            issues = self.auditor.analyze_file(str(file_path))
            
            if self.verbose:
                print(f"   Found {len(issues.get('issues', []))} issues")
            
            # STEP 2: FIX - Correct problems
            print("2. 🔧 Fixer fixing...")
            fix_result = self.fixer.fix_file(str(file_path), issues)
            
            if not fix_result.get("success", False):
                print(f"   ❌ Fix failed: {fix_result.get('error', 'Unknown error')}")
                return False
            
            # STEP 3: JUDGE - Test the fix
            print("3. 🧪 Judge testing...")
            test_result = self.judge.test_file(str(file_path))
            
            if test_result.get("success", False):
                print(f"   ✅ Tests passed!")
                return True
            else:
                print(f"   ❌ Tests failed")
                if self.verbose and "error" in test_result:
                    print(f"   Error: {test_result['error']}")
                return False
                
        except Exception as e:
            print(f"❌ Error processing {file_path.name}: {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return False
    
    def run(self):
        """Main function that runs the whole refactoring process."""
        print("\n🚀 Starting refactoring process...")
        
        # STEP 1: Find files to fix
        files_to_fix = self._discover_files()
        
        if not files_to_fix:
            print("ℹ️ No Python files found in target directory.")
            print("   (This is OK - directory might be empty for now)")
            return True  # Changed from False to True - empty is OK!
        
        # STEP 2: Create agents
        try:
            self._initialize_agents()
        except ImportError:
            print("\n💡 TIP: Test with existing test_dataset first:")
            print("   python main.py --target_dir './test_dataset' --verbose")
            return False
        
        # STEP 3: Process each file
        print("\n" + "="*60)
        print("🔄 PROCESSING FILES")
        print("="*60)
        
        total_files = len(files_to_fix)
        
        for i, file_path in enumerate(files_to_fix, 1):
            print(f"\n📊 Progress: File {i}/{total_files}")
            
            success = self._process_single_file(file_path)
            
            if success:
                self.files_processed.append(file_path)
            else:
                self.files_failed.append(file_path)
        
        # STEP 4: Show results
        print("\n" + "="*60)
        print("📊 FINAL RESULTS")
        print("="*60)
        print(f"✅ Successfully fixed: {len(self.files_processed)} files")
        print(f"❌ Failed: {len(self.files_failed)} files")
        
        if self.files_failed and self.verbose:
            print("\nFailed files:")
            for file in self.files_failed:
                print(f"   - {file.name}")
        
        # Return True if ALL files succeeded
        return len(self.files_failed) == 0


# This makes the class available to main.py
__all__ = ['RefactoringOrchestrator']
