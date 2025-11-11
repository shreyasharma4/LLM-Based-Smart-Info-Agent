from app.config import get_azure_client
from app.tools import get_agent_tools


def get_llm():
    """Return raw Azure OpenAI client, not LangChain wrapper."""
    return get_azure_client()


def get_tools():
    return get_agent_tools()
