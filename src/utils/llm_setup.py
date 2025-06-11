from langchain_google_genai import ChatGoogleGenerativeAI 
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_llm():
    """
    Checks for the Google API key and returns an instance of the 
    ChatGoogleGenerativeAI model.
    """
    # ✅ Check for the Google API key
    if "GOOGLE_API_KEY" not in os.environ:
        raise ValueError(
            "GOOGLE_API_KEY not found in environment variables. "
            "Please get a key from Google AI Studio and set it in your .env file."
        )

    return ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0) 