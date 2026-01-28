import os
import glob
import re
from typing import TypedDict, List, Annotated
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

# 1. Imports
from src.agents import Auditor, Fixer, Judge
from src.tools.code_tools import write_file_safely, run_pytest

# 2. Define State
class GraphState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    target_dir: str
    loop_count: int

# 3. Instantiate Agents
auditor = Auditor()
fixer = Fixer()
judge = Judge()

# Helper: Read the main python file from the target dir
# We assume there is at least one .py file
def get_main_file_path(target_dir):
    files = glob.glob(os.path.join(target_dir, "*.py"))
    if not files:
        return None
    # Return the first file found (or you can add logic to pick 'main.py')
    return files[0]

def read_code(target_dir):
    file_path = get_main_file_path(target_dir)
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

# Helper: Extract code from LLM response (handles markdown blocks)
def extract_code(llm_output):
    # Look for ```python ... ```
    match = re.search(r'```python\n(.*?)\n```', llm_output, re.DOTALL)
    if match:
        return match.group(1)
    # If no block, return the raw output (risky, but fallback)
    return llm_output

# 4. Define Nodes

def auditor_node(state: GraphState):
    print("--- 🕵️ Auditor Node ---")
    original_code = read_code(state["target_dir"])
    
    # Auditor only needs the code to analyze
    plan = auditor.run(original_code)
    
    return {
        "messages": [AIMessage(content=plan)],
        "loop_count": state["loop_count"]
    }

def fixer_node(state: GraphState):
    print("--- 🛠️ Fixer Node ---")
    
    original_code = read_code(state["target_dir"])
    # Get the plan from the last message (from Auditor)
    plan = state["messages"][-1].content
    
    # 1. Ask the LLM to fix the code
    fixed_code_text = fixer.run(original_code, plan)
    
    # 2. Extract clean code from the LLM response
    clean_code = extract_code(fixed_code_text)
    
    # 3. Write to disk securely
    filename = os.path.basename(get_main_file_path(state["target_dir"]))
    try:
        write_file_safely(state["target_dir"], filename, clean_code)
        status_msg = f"Code updated in {filename}"
    except Exception as e:
        status_msg = f"Error writing file: {e}"

    return {
        "messages": [AIMessage(content=status_msg)],
        "loop_count": state["loop_count"] + 1 # Increment loop count
    }

def judge_node(state: GraphState):
    print("--- ⚖️ Judge Node ---")
    
    # 1. EXECUTE UNIT TESTS (Required by Statement)
    test_output = run_pytest(state["target_dir"])
    
    # 2. Check if tests passed
    # Pytest usually returns "passed" or "failed" in the output
    # We look for "FAILED" to decide looping
    if "FAILED" in test_output or "ERROR" in test_output or "failed" in test_output:
        print("❌ Tests FAILED. Sending logs to Fixer.")
        result = f"FAIL\n\nLOGS:\n{test_output}"
    else:
        print("✅ Tests PASSED.")
        result = "SUCCESS"
        
    return {
        "messages": [AIMessage(content=result)],
        "loop_count": state["loop_count"]
    }

# 5. Logic
def should_continue(state: GraphState):
    last_message = state["messages"][-1]
    
    if state["loop_count"] >= 10:
        print("🛑 Max iterations reached.")
        return "end"
        
    if "SUCCESS" in last_message.content:
        return "end"
    else:
        return "fixer"

# 6. Build Graph
from langgraph.graph import StateGraph, END

def create_swarm_graph():
    workflow = StateGraph(GraphState)

    workflow.add_node("auditor", auditor_node)
    workflow.add_node("fixer", fixer_node)
    workflow.add_node("judge", judge_node)

    workflow.set_entry_point("auditor")

    workflow.add_edge("auditor", "fixer")
    workflow.add_edge("fixer", "judge")
    
    workflow.add_conditional_edges(
        "judge",
        should_continue,
        {
            "fixer": "fixer",
            "end": END
        }
    )

    return workflow.compile()