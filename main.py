import sys
import os
from pprint import pprint
from langchain_core.messages import HumanMessage, AIMessage

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the compiled LangGraph app
from src.graph.workflow import app

def main():
    """
    Main function to run the autonomous coding agent from the command line,
    now with conversational memory.
    """
    print("🤖 Autonomous Project Agent is ready.")
    print("Enter your project request, or type 'exit' to close.")

    # ✅ NEW: Initialize a list to store the chat history
    chat_history = []

    while True:
        prompt = input("\n> ")
        if prompt.lower() == 'exit':
            break
        
        if not prompt:
            continue

        print("\n--- Agent is building the project... ---")
        
        inputs = {
            "prompt": prompt, 
            "workspace": {}, 
            "chat_history": chat_history # Pass the current history
        }

        # We will capture the final plan to add to our history
        final_plan = ""
        for output in app.stream(inputs):
            for key, value in output.items():
                print(f"\n## Output from node '{key}':")
                pprint(value, indent=2)
                # Capture the plan when it's generated
                if key == "planner":
                    final_plan = value.get("plan")
        
        # ✅ NEW: Update the history with the latest turn
        if final_plan:
            chat_history.append(HumanMessage(content=prompt))
            chat_history.append(AIMessage(content=final_plan))

        print("\n--- Agent run complete. Check the generated files. ---\n")

if __name__ == "__main__":
    main()