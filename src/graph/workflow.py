from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict
from pprint import pformat

from src.agents.planner_agent import get_planner_agent
from src.agents.coder_agent import get_coder_agent
from src.agents.tester_agent import get_tester_agent
from src.agents.debugger_agent import get_debugger_agent
from src.tools.file_system_tools import write_files, read_file
from langchain_core.messages import BaseMessage 
from pydantic import Field 
# from src.tools.shell_tools import execute_command

class AgentState(TypedDict):
    """The state of our autonomous agent."""
    prompt: str
    plan: str
    # The workspace now holds the state of all files
    workspace: Dict[str, str] 
    test_results: str
    chat_history: List[BaseMessage] = Field(default_factory=list)

# --- Node Functions ---

def planner_node(state: AgentState) -> dict:
    planner = get_planner_agent()
    # ✅ UPDATED: Pass both the prompt and the chat history to the agent
    plan = planner.invoke({
        "prompt": state["prompt"], 
        "chat_history": state["chat_history"]
    }).content
    return {"plan": plan}

def coder_node(state: AgentState) -> dict:
    """The coder node, now aware of the workspace."""
    coder = get_coder_agent()
    result = coder.invoke({
        "plan": state["plan"],
        "workspace": pformat(state['workspace']) # Pass workspace as a string for context
    })

    # The coder MUST call the write_files tool
    if not result.tool_calls:
        raise ValueError("Coder failed to call the 'write_files' tool.")
    
    # Execute the tool call to write files to disk
    write_files.invoke(result.tool_calls[0]['args'])

    # Update the workspace in our state with the newly written files
    new_workspace = state['workspace'].copy()
    for file_info in result.tool_calls[0]['args']['files_to_write']:
        new_workspace[file_info['path']] = file_info['content']

    return {"workspace": new_workspace}


def tester_node(state: AgentState) -> dict:
    """The tester node, now acting as a code reviewer."""
    reviewer = get_tester_agent()
    
    print("---INFO: Code reviewer is analyzing the workspace...---")

    # The reviewer agent needs the original prompt and the current workspace
    review = reviewer.invoke({
        "prompt": state['prompt'],
        "workspace": pformat(state['workspace'])
    })

    # The result of the review is the text content
    test_results = review.content
    
    print(f"---INFO: Reviewer finished. Results:\n{test_results}---")
    return {"test_results": test_results}


def debugger_node(state: AgentState) -> dict:
    """The debugger node, now aware of the workspace."""
    debugger = get_debugger_agent()
    result = debugger.invoke({
        "workspace": pformat(state['workspace']),
        "test_results": state["test_results"]
    })

    if not result.tool_calls:
        raise ValueError("Debugger failed to call the 'write_files' tool.")

    # Execute the tool call to apply the fix
    write_files.invoke(result.tool_calls[0]['args'])

    # Update the workspace with the corrected files
    new_workspace = state['workspace'].copy()
    for file_info in result.tool_calls[0]['args']['files_to_write']:
        new_workspace[file_info['path']] = file_info['content']

    return {"workspace": new_workspace}

def should_continue(state: AgentState) -> str:
    """The decision-making hub. Now checks for the specific 'PASSED' keyword."""
    # We check the raw output from the reviewer.
    if state["test_results"].strip().upper() == "PASSED":
        print("---DECISION: REVIEW PASSED, FINISHING---")
        return END
    else:
        # Any other response is considered a failure that needs debugging.
        print("---DECISION: REVIEW FAILED, LOOPING TO DEBUGGER---")
        return "debugger"

# --- Graph Definition ---

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
    }
)
# After debugging, we loop back to the coder to re-evaluate and continue
workflow.add_edge("debugger", "coder")

app = workflow.compile()

# Add a default value for the workspace in the input
# app.mapper.input_schema.set_default("workspace", {})