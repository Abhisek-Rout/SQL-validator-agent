import os
from dotenv import load_dotenv

# Load environment variables at startup
load_dotenv()

def get_env(key: str, default: str = None) -> str:
    """
    Fetch environment variable safely.
    """
    return os.getenv(key, default)