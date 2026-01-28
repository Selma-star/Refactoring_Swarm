import argparse
import json
import time
from src.graph import create_swarm_graph
from src.telemetry import save_experiment_data

def main():
    # 1. Handle CLI Arguments
    parser = argparse.ArgumentParser(description="The Refactoring Swarm")
    parser.add_argument("--target_dir", required=True, help="Path to the buggy code directory")
    args = parser.parse_args()

    print(f"\n🚀 Starting Refactoring Swarm on: {args.target_dir}")
    print(f"{'='*50}\n")

    # 2. Initialize the Graph
    app = create_swarm_graph()

    # 3. Prepare Initial State
    initial_state = {
        "messages": [],
        "target_dir": args.target_dir,
        "loop_count": 0
    }

    start_time = time.time()

    # 4. Run the Swarm
    try:
        final_state = app.invoke(initial_state)
    except Exception as e:
        print(f"\n💥 CRITICAL ERROR: {e}")
        # We still try to save logs if possible, but exit with error
        final_state = initial_state # Or handle specific error logging
        final_state["error"] = str(e)

    end_time = time.time()

    # 5. Save Telemetry (Data Officer Role - 30% of Grade!)
    save_experiment_data(initial_state, final_state, start_time, end_time)

    print(f"\n{'='*50}")
    print("🏁 Swarm finished.")
    print("📊 Data saved to experiment_data.json")

if __name__ == "__main__":
    main()