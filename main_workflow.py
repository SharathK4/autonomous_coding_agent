# main_workflow.py

from langgraph.graph import StateGraph, END
from typing import TypedDict, Dict, Optional

# Import the router and compiled sub-workflows
from src.agents.router.router_agent import get_router_agent
from src.workflows.coding_workflow import get_coding_workflow
from src.workflows.blender_workflow import get_blender_workflow

# ✅ STEP 1: EXPAND THE SUPERSTATE
# The global state now includes all possible fields from all sub-graphs.
# We use 'Optional' because a field might not be used in every run.
class SuperState(TypedDict):
    """The global state for the entire application."""
    prompt: str
    destination: Optional[str]
    # Coding-specific state
    plan: Optional[str]
    workspace: Optional[Dict[str, str]]
    review: Optional[str]
    # Blender-specific state
    last_screenshot_path: Optional[str]

# Get the compiled sub-workflows and the router agent
coding_workflow = get_coding_workflow()
blender_workflow = get_blender_workflow()
router_agent = get_router_agent()

# ✅ STEP 2: UPDATE THE ROUTER NODE TO INITIALIZE STATE
def router_node(state: SuperState) -> dict:
    """The entry point router. It classifies the prompt and initializes the state for the chosen sub-graph."""
    prompt = state["prompt"]
    route = router_agent.invoke({"prompt": prompt})
    destination = route.destination
    print(f"--- Router decision: '{destination}' ---")
    
    # Initialize the state for the coding workflow
    if destination == "coding":
        return {
            "destination": "coding",
            "plan": "",
            "workspace": {},
            "review": ""
        }
    # Initialize the state for the blender workflow
    elif destination == "blender":
        return {
            "destination": "blender",
            "plan": "", # Blender agent will also have a plan
            "last_screenshot_path": ""
        }
    else:
        # Fallback if the router is confused
        return {"destination": "end"}

def should_route(state: SuperState) -> str:
    """The conditional edge logic based on the router's decision."""
    return state.get("destination", "end")

# This is the main graph that orchestrates the sub-graphs
main_workflow_graph = StateGraph(SuperState)

main_workflow_graph.add_node("router", router_node)
main_workflow_graph.add_node("coding_agent", coding_workflow)
main_workflow_graph.add_node("blender_agent", blender_workflow)

main_workflow_graph.set_entry_point("router")

main_workflow_graph.add_conditional_edges(
    "router",
    should_route,
    {
        "coding": "coding_agent",
        "blender": "blender_agent",
        "end": END,
    },
)

# After a sub-graph finishes, the workflow ends
main_workflow_graph.add_edge("coding_agent", END)
main_workflow_graph.add_edge("blender_agent", END)

# Compile the final app
app = main_workflow_graph.compile()