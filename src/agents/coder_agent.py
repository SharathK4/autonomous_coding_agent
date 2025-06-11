from langchain_core.prompts import ChatPromptTemplate
from src.utils.llm_setup import get_llm
from src.tools.file_system_tools import write_file

def get_coder_agent():
    """Returns the coder agent."""
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(
        """
        You are a master Python coder. Your task is to write Python code based on the provided plan.
        
        **Plan:**
        {plan}

        **Instructions:**
        1.  Generate the complete, correct Python code to accomplish the plan.
        2.  You MUST call the `write_file` tool to save the generated code to the correct file.
        """
    )
    return prompt | llm.bind_tools([write_file])