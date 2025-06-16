
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from src.utils.llm_setup import get_llm

def get_planner_agent():
    """
    Returns the planner agent, now aware of conversational history.
    """
    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert software development planner. Your job is to create a detailed, step-by-step plan to address the user's request.
                
                Analyze the user's request and any previous conversation history. If the user is providing a correction or clarification, prioritize that information.
                
                The plan should be clear, concise, and sufficient for a coding agent to execute. Do not generate code, only the plan.""",
            ),
            
            MessagesPlaceholder(variable_name="chat_history"),
            (
                "human",
                "{prompt}",
            ),
        ]
    )
    return prompt | llm