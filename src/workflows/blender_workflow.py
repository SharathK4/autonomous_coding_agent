from langgraph.graph import StateGraph, END
from typing import TypedDict
from src.agents.blender.executor_agent import get_executor_agent
from src.tools.blender_tools import connect_to_blender, send_blender_command, disconnect_from_blender

class BlenderState(TypedDict):
    prompt: str
    result: str

def connect_node(state):
    print("---CONNECTING TO BLENDER---")
    connection_result = connect_to_blender.invoke({})
    if "Error" in connection_result:
        raise ConnectionError(connection_result)
    return {"result": connection_result}

def executor_node(state):
    print("---GENERATING & SENDING BLENDER COMMAND---")
    agent = get_executor_agent()
    result = agent.invoke({"prompt": state["prompt"]})
    
    
    if not result.tool_calls:
        raise ValueError("Blender Executor agent failed to generate a command.")
        
    
    command_result = send_blender_command.invoke(result.tool_calls[0]['args'])
    return {"result": command_result}

def disconnect_node(state):
    print("---DISCONNECTING FROM BLENDER---")
    result = disconnect_from_blender.invoke({})
    return {"result": result}

def get_blender_workflow():
    workflow = StateGraph(BlenderState)

    workflow.add_node("connect", connect_node)
    workflow.add_node("executor", executor_node)
    workflow.add_node("disconnect", disconnect_node)

    workflow.set_entry_point("connect")
    workflow.add_edge("connect", "executor")
    workflow.add_edge("executor", "disconnect")
    workflow.add_edge("disconnect", END)
    
    return workflow.compile()