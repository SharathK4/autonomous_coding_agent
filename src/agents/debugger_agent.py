from langchain_core.prompts import ChatPromptTemplate
from src.utils.llm_setup import get_llm 
from src.tools.file_system_tools import write_file, read_file 

def get_debugger_agent():
    """Returns the debugger agent."""
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(
        """
        You are a debugger agent. You need to fix the provided code based on the test results.
        File to debug: {file_path}
        Test Results:
        {test_results}

        Read the file, fix the code, and use the provided tool to write the corrected code back to the file.
        """
    )
    return prompt | llm.bind_tools([read_file, write_file])