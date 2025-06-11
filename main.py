import sys
import os
from pprint import pprint

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the compiled LangGraph app
from src.graph.workflow import app

def main():
    """
    Main function to run the autonomous coding agent from the command line.
    """
    print("🤖 Autonomous Coding Agent is ready.")
    print("Enter your coding request, or type 'exit' to close.")

    while True:
        prompt = input("\n> ")
        if prompt.lower() == 'exit':
            break
        
        if not prompt:
            continue

        print("\n--- Agent is thinking... ---")
        
        # Prepare the inputs for the LangGraph agent
        inputs = {"prompt": prompt}

        # The 'stream' method will run the agent and automatically send
        # traces to LangSmith because of the environment variables.
        for output in app.stream(inputs):
            # Print output to the console as it runs
            for key, value in output.items():
                print(f"\n## Output from node '{key}':")
                pprint(value, indent=2)
        
        print("\n--- Agent run complete. Check LangSmith for detailed traces. ---\n")


if __name__ == "__main__":
    main()