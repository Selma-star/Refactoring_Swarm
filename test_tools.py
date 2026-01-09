from src.tools.analysis_tools import run_pylint
import os

# Create a small file to test
test_file = "sandbox/verify_me.py"
os.makedirs("sandbox", exist_ok=True)
with open(test_file, "w") as f:
    f.write("import os\ndef test():\n    x = 10\n    return x")

print("🚀 Running Toolsmith Final Verification...")
report = run_pylint(test_file)

print("\n--- PYLINT REPORT START ---")
print(report)
print("--- PYLINT REPORT END ---")

if "Module verify_me" in report or "rated at" in report:
    print("\n✅ SUCCESS: The Toolsmith is ready!")
else:
    print("\n❌ FAILED: Still not getting the report.")