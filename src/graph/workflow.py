from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from src.agents.planner_agent import get_planner_agent
from src.agents.coder_agent import get_coder_agent
from src.agents.tester_agent import get_tester_agent
from src.agents.debugger_agent import get_debugger_agent

from src.tools.file_system_tools import write_file 

class AgentState(TypedDict):
    prompt: str
    plan: str
    file_path: str
    test_results: str
    code: str

# ... (planner_node and AgentState are unchanged) ...
def planner_node(state):
    planner = get_planner_agent()
    plan = planner.invoke({"prompt": state["prompt"]}).content
    return {"plan": plan}

# ...

def coder_node(state):
    """
    Generates code and handles both tool calls and direct code output.
    """
    coder = get_coder_agent()
    result = coder.invoke({"plan": state["plan"]})
    
    # ✅ SAFEGUARD: Check if the LLM used the tool
    if result.tool_calls:
        # If the tool was called, extract details from it
        tool_call = result.tool_calls[0]
        file_path = tool_call['args']['file_path']
        code = tool_call['args']['content']
        # Actually execute the file write here
        write_file.invoke(tool_call['args'])
        print(f"---INFO: Coder called write_file tool for {file_path}---")
    else:
        # If the tool was NOT called, extract the code from the content
        # and create a default file path.
        code = result.content
        file_path = "app.py" # A reasonable default
        # Manually call the write_file tool
        write_file.invoke({"file_path": file_path, "content": code})
        print(f"---INFO: Coder did not use tool. Manually saving to {file_path}---")

    return {"file_path": file_path, "code": code}

# ... (tester_node, debugger_node, and the rest of the file are unchanged) ...
def tester_node(state):
    tester = get_tester_agent()
    # For testing, we'll try to run the file
    command_to_run = f"python {state['file_path']}"
    test_results = tester.invoke({"file_path": state["file_path"], "command": command_to_run}).content
    print(f"---INFO: Tester executed command: '{command_to_run}'---")
    return {"test_results": test_results}

def debugger_node(state):
    debugger = get_debugger_agent()
    # The debugger will now get the file_path and test_results to work with
    result = debugger.invoke({"file_path": state["file_path"], "test_results": state["test_results"]})
    
    # Similar to the coder, we must handle the debugger's output
    if result.tool_calls:
        tool_call = result.tool_calls[0]
        # Execute the file write with the corrected code
        write_file.invoke(tool_call['args'])
        print(f"---INFO: Debugger called write_file tool for {tool_call['args']['file_path']}---")
    else:
        print("---WARNING: Debugger did not call a tool to fix the code.---")
        
    return {} # Return an empty dict as it loops back to the coder

def should_continue(state):
    # More robust error checking
    test_output = state["test_results"].lower()
    if "error" in test_output or "traceback" in test_output or "not found" in test_output:
        print("---DECISION: ERRORS DETECTED, MOVING TO DEBUGGER---")
        return "debugger"
    else:
        print("---DECISION: TESTS PASSED (OR NO ERRORS DETECTED), FINISHING---")
        return END


workflow = StateGraph(AgentState)

workflow.add_node("planner", planner_node)
workflow.add_node("coder", coder_node)
workflow.add_node("tester", tester_node)
workflow.add_node("debugger", debugger_node)

workflow.set_entry_point("planner")
workflow.add_edge("planner", "coder")
workflow.add_edge("coder", "tester")
workflow.add_conditional_edges(
    "tester",
    should_continue,
    {
        "debugger": "debugger",
        END: END,
    },
)
workflow.add_edge("debugger", "coder")

app = workflow.compile()