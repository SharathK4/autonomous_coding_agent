# src/workflows/coding_workflow.py

from langgraph.graph import StateGraph, END
from typing import TypedDict, Dict
from pprint import pformat

# Import the specialized coding agents and tools
from src.agents.coding.planner_agent import get_planner_agent
from src.agents.coding.coder_agent import get_coder_agent
from src.agents.coding.tester_agent import get_tester_agent
from src.agents.coding.debugger_agent import get_debugger_agent
from src.tools.file_system_tools import write_files

# 1. Define the state for this specific workflow
class CodingState(TypedDict):
    """
    Represents the state of the coding workflow. This is the "memory"
    for all coding-related tasks.
    """
    prompt: str
    plan: str
    workspace: Dict[str, str]
    review: str  # This will hold the output from the reviewer agent

# 2. Define the node functions for the graph
def planner_node(state: CodingState) -> dict:
    """Generates the initial plan."""
    print("---PLANNER---")
    planner = get_planner_agent()
    plan = planner.invoke({"prompt": state["prompt"]}).content
    return {"plan": plan}

def coder_node(state: CodingState) -> dict:
    """Generates code based on the plan and current workspace."""
    print("---CODER---")
    coder = get_coder_agent()
    result = coder.invoke({
        "plan": state["plan"],
        "workspace": pformat(state['workspace'])
    })

    if not result.tool_calls:
        raise ValueError("Coder failed to call the 'write_files' tool.")
    
    # Execute the tool call to write files to disk
    write_files.invoke(result.tool_calls[0]['args'])

    # Update the workspace in our state
    new_workspace = state['workspace'].copy()
    for file_info in result.tool_calls[0]['args']['files_to_write']:
        new_workspace[file_info['path']] = file_info['content']

    return {"workspace": new_workspace}

def reviewer_node(state: CodingState) -> dict:
    """Acts as a code reviewer to check for correctness."""
    print("---REVIEWER---")
    reviewer = get_tester_agent()
    review_result = reviewer.invoke({
        "prompt": state['prompt'],
        "workspace": pformat(state['workspace'])
    }).content
    print(f"Reviewer result: {review_result}")
    return {"review": review_result}

def debugger_node(state: CodingState) -> dict:
    """Generates fixes for the code based on the review."""
    print("---DEBUGGER---")
    debugger = get_debugger_agent()
    result = debugger.invoke({
        "workspace": pformat(state['workspace']),
        "review": state["review"]
    })

    if not result.tool_calls:
        raise ValueError("Debugger failed to call the 'write_files' tool.")

    write_files.invoke(result.tool_calls[0]['args'])

    new_workspace = state['workspace'].copy()
    for file_info in result.tool_calls[0]['args']['files_to_write']:
        new_workspace[file_info['path']] = file_info['content']

    return {"workspace": new_workspace}

def should_continue(state: CodingState) -> str:
    """The conditional logic to decide to end or loop."""
    if state["review"].strip().upper() == "PASSED":
        print("---DECISION: CODING COMPLETE---")
        return END
    else:
        print("---DECISION: REVIEW FAILED, LOOPING TO DEBUGGER---")
        return "debugger"

# 3. Define the factory function that creates and compiles the graph
def get_coding_workflow():
    """
    Builds and compiles the stateful graph for the coding agent.
    Returns a compiled LangGraph app.
    """
    workflow = StateGraph(CodingState)

    # Add nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("coder", coder_node)
    workflow.add_node("reviewer", reviewer_node)
    workflow.add_node("debugger", debugger_node)

    # Define edges
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "coder")
    workflow.add_edge("coder", "reviewer")
    workflow.add_edge("debugger", "coder") # After debugging, go back to the coder

    # Define the conditional edge for the main loop
    workflow.add_conditional_edges(
        "reviewer",
        should_continue,
        {
            "debugger": "debugger",
            END: END,
        },
    )

    # Compile the graph into a runnable app
    return workflow.compile()