import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime
import sys
from typing import Optional, Dict, Any

class Logger:
    def __init__(self):
        # Print startup banner immediately
        print("*" * 80)
        print("               BEYKENT EXAM RESULT NOTIFIER STARTING                ")
        print("*" * 80)
        
        # Create logs directory if it doesn't exist
        self.log_directory = "logs"
        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)

        # Initialize logger
        self.logger = logging.getLogger("beykent_exam_notifier")
        self.logger.setLevel(logging.DEBUG)

        # Configure logging format
        self.log_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Set up handlers
        self._setup_file_handler()
        self._setup_console_handler()
        self._setup_error_handler()

    def _setup_file_handler(self) -> None:
        """Set up the main rotating file handler"""
        file_handler = RotatingFileHandler(
            filename=os.path.join(self.log_directory, "app.log"),
            maxBytes=5*1024*1024,  # 5MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(self.log_format)
        file_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)

    def _setup_console_handler(self) -> None:
        """Set up console output handler"""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.log_format)
        console_handler.setLevel(logging.INFO)
        self.logger.addHandler(console_handler)

    def _setup_error_handler(self) -> None:
        """Set up separate error log handler"""
        error_handler = RotatingFileHandler(
            filename=os.path.join(self.log_directory, "error.log"),
            maxBytes=5*1024*1024,
            backupCount=3,
            encoding='utf-8'
        )
        error_handler.setFormatter(self.log_format)
        error_handler.setLevel(logging.ERROR)
        self.logger.addHandler(error_handler)

    def debug(self, message: str) -> None:
        """Log debug message"""
        self.logger.debug(message)

    def info(self, message: str) -> None:
        """Log info message"""
        self.logger.info(message)

    def warning(self, message: str) -> None:
        """Log warning message"""
        self.logger.warning(message)

    def error(self, message: str, exc_info: bool = True) -> None:
        """Log error message"""
        self.logger.error(message, exc_info=exc_info)

    def critical(self, message: str) -> None:
        """Log critical message"""
        self.logger.critical(message, exc_info=True)

    def log_request_response(self, request_type: str, details: str, 
                           response: Optional[str] = None, 
                           error: Optional[Exception] = None) -> None:
        """Log API/Selenium requests and responses"""
        msg = f"Request [{request_type}]: {details}"
        if response:
            msg += f"\nResponse: {response}"
        if error:
            msg += f"\nError: {str(error)}"
        self.debug(msg)

    def log_operation_time(self, operation_name: str, start_time: datetime) -> None:
        """Log operation execution time"""
        execution_time = datetime.now() - start_time
        self.info(f"Operation [{operation_name}] took {execution_time.total_seconds():.2f} seconds")

    def log_error_with_context(self, error: Exception, context: Optional[Dict[str, Any]] = None) -> None:
        """Log errors with additional context"""
        error_msg = f"Error: {str(error)}"
        if context:
            error_msg += f"\nContext: {context}"
        self.error(error_msg)

# Create singleton instance
logger = Logger()