import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

def get_azure_client():
    """Return raw Azure OpenAI client for direct completions."""
    return AzureOpenAI(
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_KEY")
    )
