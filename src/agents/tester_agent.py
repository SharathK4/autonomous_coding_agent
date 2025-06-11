from langchain_core.prompts import ChatPromptTemplate
from src.utils.llm_setup import get_llm 
from src.tools.shell_tools import execute_command  

def get_tester_agent():
    """Returns the tester agent."""
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(
        """
        You are a tester agent. Your job is to test the provided code.
        You have access to a shell to execute the code.
        Code to test is located at: {file_path}

        Execute the code and analyze the output for errors.
        If there are errors, describe them clearly. If the code runs successfully, confirm it.
        """
    )
    return prompt | llm.bind_tools([execute_command])