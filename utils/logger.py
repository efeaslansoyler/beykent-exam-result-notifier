import logging
from logging.handlers import RotatingFileHandler
import os

# Get the logs directory from environment variables
logs_dir = "logs"

# Create logs directory if it doesn't exist
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

def setup_logger(name: str = "beykent_exam_notifier") -> logging.Logger:
    """
    Configure and return a logger instance with rotating file and console handlers.
    
    Args:
        name (str): The name of the logger. Defaults to "beykent_exam_notifier"
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logger instance
    logger = logging.getLogger(name)
    
    # Remove any existing handlers to avoid duplicates
    logger.handlers = []
    
    # Set the base logging level to DEBUG to capture all messages
    logger.setLevel(logging.DEBUG)
    
    # Define the format for log messages
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                                datefmt='%Y-%m-%d %H:%M:%S')
    
    # Set up rotating file handler (10 MB max size)
    file_handler = RotatingFileHandler(
        os.path.join(logs_dir, "app.log"),
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=1  # Keep one backup file
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Set up console handler to show logs in terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # Show all logs in console
    console_handler.setFormatter(formatter)
    
    # Add both handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Add a separation line to indicate new application run
    logger.info("="*80)
    logger.info("Application Started")
    logger.info("="*80)
    
    return logger

# Create a default logger instance
logger = setup_logger()