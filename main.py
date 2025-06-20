from pprint import pprint
from langchain_core.messages import HumanMessage, AIMessage

from main_workflow import app

def main():
    print("\n AI Agent is ready.")
    print("Enter your request for coding or Blender, or type 'exit' to close.")

    chat_history = []

    while True:
        prompt = input("\n> ")
        if prompt.lower() == 'exit':
            break
        
        if not prompt:
            continue

        print("\n--- Agent is routing and executing... ---")
        
        inputs = {"prompt": prompt, "chat_history": chat_history}
        final_state = None
        for output in app.stream(inputs):
            pprint(output)
            print("---")
            final_state = output

        chat_history.append(HumanMessage(content=prompt))
        
        if final_state:
            
            last_agent_key = [key for key in final_state if key != 'router'][-1]
            agent_response = final_state[last_agent_key]
            chat_history.append(AIMessage(content=str(agent_response)))

        print("\n--- Agent run complete. Ready for your next message. ---\n")
        
        print("\n--- Agent run complete. ---\n")

if __name__ == "__main__":
    main()