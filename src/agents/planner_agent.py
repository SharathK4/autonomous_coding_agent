from langchain_core.prompts import ChatPromptTemplate
from src.utils.llm_setup import get_llm  
def get_planner_agent():
    """Returns the planner agent."""
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(
        """
        You are a planner agent. Your role is to break down a user's request into a series of actionable steps.
        Provide a clear and concise plan to address the following prompt:
        {prompt}
        """
    )
    return prompt | llm