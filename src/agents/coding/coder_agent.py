

from langchain_core.prompts import ChatPromptTemplate
from src.utils.llm_setup import get_llm
from src.tools.file_system_tools import write_files, read_file 

def get_coder_agent():
    """Returns the coder agent, now aware of the project workspace."""
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(
        """
        You are a master programmer building a full software project.
        You have been given a plan and the current state of the project's file workspace.
        Your task is to generate the code for the next step.

        **Current Project Workspace:**
        {workspace}

        **Plan:**
        {plan}

        **Instructions:**
        1.  Analyze the plan and the existing files in the workspace.
        2.  Generate all necessary new files or modifications to existing files.
        3.  You MUST use the `write_files` tool to save all your changes. The input is a list of dictionaries, each with 'path' and 'content'.
        4.  If you need to read a file for context, use the `read_file` tool first.
        """
    )
    
    return prompt | llm.bind_tools([write_files, read_file])