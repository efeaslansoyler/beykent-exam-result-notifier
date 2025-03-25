import logging
import os
from utils.config import get_env_var

# Get the logs directory from environment variables
logs_dir = get_env_var("LOGS_FOLDER")

# Create logs directory if it doesn't exist
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

def setup_logger(name: str = "beykent_exam_notifier") -> logging.Logger:
    """
    Configure and return a logger instance with file and console handlers.
    
    Args:
        name (str): The name of the logger. Defaults to "beykent_exam_notifier"
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logger instance
    logger = logging.getLogger(name)
    
    # Set the base logging level to DEBUG to capture all messages
    logger.setLevel(logging.DEBUG)
    
    # Define the format for log messages
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                                datefmt='%Y-%m-%d %H:%M:%S')
    
    # Set up file handler to write logs to file
    file_handler = logging.FileHandler(os.path.join(logs_dir, "app.log"))
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Add the file handler to the logger
    logger.addHandler(file_handler)
    
    # Add a separation line to indicate new application run
    logger.info("="*80)
    logger.info("Application Started")
    logger.info("="*80)
    
    return logger

# Create a default logger instance
logger = setup_logger()