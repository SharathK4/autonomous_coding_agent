# src/agents/router/router_agent.py

from langchain_core.prompts import ChatPromptTemplate
from pydantic  import BaseModel, Field
from src.utils.llm_setup import get_llm

class RouteQuery(BaseModel):
    """Routes a user query to the appropriate workflow."""
    destination: str = Field(
        ...,
        description="The destination workflow to route the user's query to.",
        enum=["coding", "blender"],
    )

def get_router_agent():
    """
    An agent that decides whether a prompt is for the 'coding' workflow
    or the 'blender' workflow.
    """
    llm = get_llm()
    structured_llm = llm.with_structured_output(RouteQuery)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", 
         "You are an expert at routing a user's request to the correct workflow."
         "The 'coding' workflow is for creating and modifying software projects with code and text files."
         "The 'blender' workflow is for automating tasks in the 3D software, Blender."),
        ("human", "{prompt}")
    ])
    
    return prompt | structured_llm