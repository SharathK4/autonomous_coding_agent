import sys
import os
from pprint import pprint

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the master app from the main_workflow file
from main_workflow import app

def main():
    print("🤖 Versatile AI Agent is ready.")
    print("Enter your request for coding or Blender, or type 'exit' to close.")

    while True:
        prompt = input("\n> ")
        if prompt.lower() == 'exit':
            break
        
        if not prompt:
            continue

        print("\n--- Agent is routing and executing... ---")
        
        # The input state is now very simple
        inputs = {"prompt": prompt}

        for output in app.stream(inputs):
            pprint(output)
            print("---")
        
        print("\n--- Agent run complete. ---\n")

if __name__ == "__main__":
    main()