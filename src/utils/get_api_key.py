from dotenv import load_dotenv
import os


GROQ_API_KEY = None


def get_groq_api_key() -> str:
    """
    """
    global GROQ_API_KEY

    if not GROQ_API_KEY:
        load_dotenv(override=True)
        GROQ_API_KEY = os.getenv(key="GROQ_API_KEY")

    return GROQ_API_KEY
