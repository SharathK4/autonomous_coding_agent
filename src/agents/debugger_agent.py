# from langchain_core.prompts import ChatPromptTemplate
# from src.utils.llm_setup import get_llm 
# from src.tools.file_system_tools import write_file, read_file 

# def get_debugger_agent():
#     """Returns the debugger agent."""
#     llm = get_llm()
#     prompt = ChatPromptTemplate.from_template(
#         """
#         You are a debugger agent. You need to fix the provided code based on the test results.
#         File to debug: {file_path}
#         Test Results:
#         {test_results}

#         Read the file, fix the code, and use the provided tool to write the corrected code back to the file.
#         """
#     )
#     return prompt | llm.bind_tools([read_file, write_file])

from langchain_core.prompts import ChatPromptTemplate
from src.utils.llm_setup import get_llm
from src.tools.file_system_tools import write_files, read_file

def get_debugger_agent():
    """Returns the debugger agent, aware of the full workspace."""
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(
        """
        You are a senior debugging engineer. The project has failed a test.
        Your job is to analyze the entire project workspace and the test results to find and fix the bug.

        **Current Project Workspace:**
        {workspace}

        **Test Results That Failed:**
        {test_results}

        **Instructions:**
        1.  Carefully review the test results and all files in the workspace to understand the root cause of the error.
        2.  Generate the corrected code for one or more files.
        3.  You MUST use the `write_files` tool to apply your fixes.
        """
    )
    return prompt | llm.bind_tools([write_files, read_file])