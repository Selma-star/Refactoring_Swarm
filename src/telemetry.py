import json
import datetime
import os

def save_experiment_data(initial_state, final_state, start_time, end_time):
    """
    Records the execution of the swarm in experiment_data.json
    """
    
    # 1. Prepare the Data Structure
    data = {
        "metadata": {
            "start_time": datetime.datetime.fromtimestamp(start_time).isoformat(),
            "end_time": datetime.datetime.fromtimestamp(end_time).isoformat(),
            "duration_seconds": end_time - start_time,
            "target_dir": initial_state["target_dir"],
            "total_iterations": final_state.get("loop_count", 0)
        },
        "history": [], # We will fill this with agent actions
        "result": {
            "status": "FAILED",
            "final_message": "",
            "error": None
        }
    }

    # 2. Convert LangGraph messages to a readable log format
    # We iterate over the messages in the final state to build the history
    # 2. Convert LangGraph messages to a readable log format
    for msg in final_state.get("messages", []):
        agent_type = "Unknown"
        content_preview = ""
        
        if hasattr(msg, 'content'):
            content_preview = msg.content[:200] + "..." if len(msg.content) > 200 else msg.content
            
            # We look for keywords we know are in the graph.py messages
            if "Code updated" in msg.content or "Error writing file" in msg.content:
                agent_type = "Fixer"
            elif "SUCCESS" in msg.content or "FAIL" in msg.content or "LOGS" in msg.content:
                agent_type = "Judge"
            else:
                # Default assumption for the first analysis
                agent_type = "Auditor"

        entry = {
            "agent": agent_type,
            "type": type(msg).__name__,
            "timestamp": datetime.datetime.now().isoformat(),
            "content_preview": content_preview
        }
        data["history"].append(entry)
      # 3. Determine Final Status
    if "error" in final_state:
        data["result"]["status"] = "CRASHED"
        data["result"]["error"] = final_state["error"]
    elif final_state.get("messages"):
        last_msg = final_state["messages"][-1].content
        if "SUCCESS" in last_msg:
            data["result"]["status"] = "SUCCESS"
        else:
            data["result"]["status"] = "FAILED (Max Iterations or Logic Error)"
    
    data["result"]["final_message"] = final_state.get("messages", [])[-1].content if final_state.get("messages") else ""

    # 4. Write to file
    output_path = "experiment_data.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    
    print(f"✅ Telemetry saved to {output_path}")