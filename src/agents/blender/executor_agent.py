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
        You are an expert-level Blender Python API (`bpy`) programmer. Your sole purpose is to convert a user's request into a single, executable snippet of Python code and call a tool with it.

        **User Request:**
        {prompt}

        **Your Task:**
        1.  Analyze the user's request.
        2.  Write a self-contained Python code snippet that performs the requested action using the `bpy` API.
        3.  You MUST call the `send_blender_command` tool with your generated code.
        4.  DO NOT write explanations, comments, or any conversational text. Your only output must be the tool call.

        ```
        """
    )
    # By only binding this one tool, we heavily encourage the agent to use it.
    return prompt | llm.bind_tools([send_blender_command])