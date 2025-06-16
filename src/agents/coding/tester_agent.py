from langchain_core.prompts import ChatPromptTemplate
from src.utils.llm_setup import get_llm


def get_tester_agent():
    """
    Returns a Code Reviewer agent.
    This agent reviews the code in the workspace to see if it meets the prompt's requirements.
    """
    llm = get_llm()
    
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
    
    return prompt | llm