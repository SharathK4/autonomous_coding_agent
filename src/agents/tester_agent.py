# from langchain_core.prompts import ChatPromptTemplate
# from src.utils.llm_setup import get_llm 
# from src.tools.shell_tools import execute_command  

# def get_tester_agent():
#     """Returns the tester agent."""
#     llm = get_llm()
#     prompt = ChatPromptTemplate.from_template(
#         """
#         You are a tester agent. Your job is to test the provided code.
#         You have access to a shell to execute the code.
#         Code to test is located at: {file_path}

#         Execute the code and analyze the output for errors.
#         If there are errors, describe them clearly. If the code runs successfully, confirm it.
#         """
#     )
#     return prompt | llm.bind_tools([execute_command])

# # src/agents/tester_agent.py

# from langchain_core.prompts import ChatPromptTemplate
# from src.utils.llm_setup import get_llm
# from src.tools.shell_tools import execute_command

# def get_tester_agent():
#     """Returns the tester agent."""
#     llm = get_llm()
#     # ✅ UPDATED PROMPT: Now expects a 'command' instead of a 'file_path'.
#     prompt = ChatPromptTemplate.from_template(
#         """
#         You are a Quality Assurance (QA) engineer. 
#         Your task is to test a software project by running a shell command.

#         **Command to Execute:**
#         {command}

#         **Instructions:**
#         1.  You have been given a command to execute.
#         2.  Use the `execute_command` tool to run it.
#         3.  Analyze the output (stdout and stderr).
#         4.  If the output contains any errors, tracebacks, or failure messages, report them clearly.
#         5.  If the command executes without any error messages, confirm that the test has passed.
#         """
#     )
#     # The tester only needs the ability to execute commands.
#     return prompt | llm.bind_tools([execute_command])


# src/agents/tester_agent.py

from langchain_core.prompts import ChatPromptTemplate
from src.utils.llm_setup import get_llm
# No tools are needed for this agent anymore, as it only "thinks".

def get_tester_agent():
    """
    Returns a Code Reviewer agent.
    This agent reviews the code in the workspace to see if it meets the prompt's requirements.
    """
    llm = get_llm()
    # ✅ A much more intelligent prompt for code review.
    prompt = ChatPromptTemplate.from_template(
        """
        You are a senior software engineer and expert code reviewer.
        Your task is to review the code in the workspace and determine if it meets the user's original request.

        **User's Original Request:**
        {prompt}

        **Current Project Workspace (Code):**
        {workspace}

        **Review Checklist:**
        1.  Does the code address all key aspects of the user's prompt?
        2.  Is the code free of obvious syntax errors or logical bugs?
        3.  For multi-file projects, are the imports and exports set up correctly between files?

        **Your Output:**
        - If the code is correct and complete, respond with only the word "PASSED".
        - If the code is incorrect or has bugs, provide a short, clear description of the error or the missing part. This will be sent to the debugger. DO NOT respond with "PASSED".
        """
    )
    # This agent doesn't need tools, it just provides a text analysis.
    return prompt | llm