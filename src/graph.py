import os
import glob
import re
from typing import TypedDict, List, Annotated, Optional
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

# 1. Imports
from src.agents import Auditor, Fixer, Judge
from src.tools.code_tools import write_file_safely, run_pytest, run_pylint

# 2. Define State
class GraphState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    target_dir: str
    loop_count: int
    current_pylint_score: float
    # We track the previous score to detect if we are "Stuck"
    previous_pylint_score: Optional[float]

# 3. Instantiate Agents
auditor = Auditor()
fixer = Fixer()
judge = Judge()

# --- Helpers ---
def get_main_file_path(target_dir):
    files = glob.glob(os.path.join(target_dir, "*.py"))
    code_files = [f for f in files if "test_" not in f]
    if code_files:
        return code_files[0]
    return files[0] if files else None

def read_code(target_dir):
    file_path = get_main_file_path(target_dir)
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def extract_pylint_score(pylint_output):
    match = re.search(r'rated at (\d+\.\d+)', pylint_output)
    if match:
        return float(match.group(1))
    return 0.0

def extract_code(llm_output):
    match = re.search(r'```python\n(.*?)\n```', llm_output, re.DOTALL)
    if match:
        return match.group(1)
    return llm_output

# 4. Nodes

def auditor_node(state: GraphState):
    print(f"\n{'='*20} ITERATION {state['loop_count']} {'='*20}")
    print("🧠 Auditor is analyzing the code...")
    
    # Run Pylint
    pylint_output = run_pylint(state["target_dir"])
    current_score = extract_pylint_score(pylint_output)
    print(f"📊 Current Code Quality: {current_score}/10")
    
    # Ask Auditor
    original_code = read_code(state["target_dir"])
    plan = auditor.run(original_code)
    
    return {
        "messages": [AIMessage(content=plan)],
        "loop_count": state["loop_count"],
        "current_pylint_score": current_score,
        "previous_pylint_score": state.get("previous_pylint_score") # Keep previous if exists
    }

def fixer_node(state: GraphState):
    print(f"🛠️ Fixer Node (Loop #{state['loop_count']})...")
    
    original_code = read_code(state["target_dir"])
    plan = state["messages"][-1].content
    
    # 1. Generate Fix
    fixed_code_text = fixer.run(original_code, plan)
    clean_code = extract_code(fixed_code_text)
    
    # 2. Write File
    filename = os.path.basename(get_main_file_path(state["target_dir"]))
    try:
        write_file_safely(state["target_dir"], filename, clean_code)
        print(f"✅ Updated file: {filename}")
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return {
            "messages": [AIMessage(content=f"Error: {e}")],
            "loop_count": state["loop_count"] + 1,
            "current_pylint_score": state["current_pylint_score"],
            "previous_pylint_score": state["current_pylint_score"]
        }

    # 3. Measure NEW Score
    pylint_output = run_pylint(state["target_dir"])
    new_score = extract_pylint_score(pylint_output)
    print(f"📈 New Score: {new_score}/10 (Previous: {state['current_pylint_score']}/10)")
    
    return {
        "messages": [AIMessage(content=f"Code updated. New score: {new_score}")],
        "loop_count": state["loop_count"] + 1,
        "current_pylint_score": new_score,
        # The OLD current_score becomes the NEW previous_score
        "previous_pylint_score": state["current_pylint_score"] 
    }

def judge_node(state: GraphState):
    print("⚖️ Judge is running Unit Tests...")
    test_output = run_pytest(state["target_dir"])
    
    if "FAILED" in test_output or "ERROR" in test_output:
        print("❌ Tests FAILED. Fixing...")
        result = f"FAIL\n\nLOGS:\n{test_output}"
    else:
        result = "SUCCESS"
        
    return {
        "messages": [AIMessage(content=result)],
        "loop_count": state["loop_count"],
        "current_pylint_score": state["current_pylint_score"],
        "previous_pylint_score": state.get("previous_pylint_score")
    }

# 5. Decision Logic

def decide_after_auditor(state: GraphState):
    auditor_message = state["messages"][-1].content.lower()
    if any(keyword in auditor_message for keyword in ["no changes needed", "code is perfect", "no bugs"]):
        print("✋ Auditor says code is perfect. Skipping Fixer.")
        return "judge"
    return "fixer"

def should_continue(state: GraphState):
    last_message = state["messages"][-1].content
    current_score = state["current_pylint_score"]
    prev_score = state.get("previous_pylint_score")
    
    # A. Check Test Failures
    if "FAIL" in last_message:
        return "fixer"

    # B. Check Max Iterations
    if state["loop_count"] >= 10:
        print("🛑 Max iterations reached. Stopping.")
        return "end"

    # C. Check Score Quality
    if current_score >= 9.5:
        print(f"👑 Target reached ({current_score}/10). Success!")
        return "end"

    # D. Check for "Stuck" Score (Diminishing Returns)
    # If the score is exactly the same as 2 loops ago, we are stuck.
    if prev_score is not None and current_score == prev_score:
        print(f"🔄 Score is stuck at {current_score}/10. No improvement detected.")
        print("🛑 Stopping to prevent infinite loop.")
        return "end"

    # E. Continue Loop
    print(f"🔄 Score {current_score}/10 needs improvement. Looping...")
    return "fixer"

# 6. Build Graph
from langgraph.graph import StateGraph, END

def create_swarm_graph():
    workflow = StateGraph(GraphState)
    workflow.add_node("auditor", auditor_node)
    workflow.add_node("fixer", fixer_node)
    workflow.add_node("judge", judge_node)
    workflow.set_entry_point("auditor")

    workflow.add_conditional_edges("auditor", decide_after_auditor, {"fixer": "fixer", "judge": "judge"})
    workflow.add_edge("fixer", "judge")
    
    workflow.add_conditional_edges("judge", should_continue, {"fixer": "fixer", "end": END})

    return workflow.compile()