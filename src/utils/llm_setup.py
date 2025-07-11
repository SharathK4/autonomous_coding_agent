from langchain_google_genai import ChatGoogleGenerativeAI 
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    """
    Checks for the Google API key and returns an instance of the ChatGoogleGenerativeAI model.
    """

    if "GOOGLE_API_KEY" not in os.environ:
        raise ValueError(
            "GOOGLE_API_KEY not found"
        )

    return ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0) 

