from dotenv import load_dotenv
import os

load_dotenv()

def get_env_var(key: str, default: str = None) -> str | bool:
    """
    Get environment variable value with type conversion for booleans.
    
    Args:
        key (str): Environment variable key
        default (str): Default value if key not found
        
    Returns:
        str | bool: Value of environment variable, or default if not found
                   Returns bool for 'true'/'false' values, str otherwise
    """
    value = os.getenv(key, default)
    if isinstance(value, str):
        # Convert boolean strings to actual boolean values
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
    return value
