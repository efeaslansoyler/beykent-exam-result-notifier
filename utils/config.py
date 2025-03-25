from dotenv import load_dotenv
import os

load_dotenv()

def get_env_var(key: str, default: str = None) -> str:
    return os.getenv(key, default)
