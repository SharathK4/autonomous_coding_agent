# src/agents/blender/executor_agent.py

from langchain_core.prompts import ChatPromptTemplate
from src.utils.llm_setup import get_llm
from src.tools.blender_tools import send_blender_command

def get_executor_agent():
    """
    This agent takes a single step from a plan and generates the
    `bpy` Python code to execute it in a live Blender session.
    """
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(
        """
        You are an expert Blender Python API (`bpy`) programmer.
        Your task is to convert a single, high-level user request into a small, executable
        snippet of Python code that can be sent to a live Blender instance.

        **User Request:**
        {prompt}

        **Instructions:**
        - Generate only the Python code required to perform this action.
        - Do not include any explanations, only the code.
        - The code must be self-contained and ready to execute. For example, always `import bpy`.
        - Use the `send_blender_command` tool to send your generated code to Blender.

        Example:
        User Request: "create a cube"
        Your code output:
        import bpy
        bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
        """
    )
    return prompt | llm.bind_tools([send_blender_command])