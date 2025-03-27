import time
import sys
from datetime import datetime
from typing import Optional

from pages.login_page import LoginPage
from pages.results_page import ResultsPage
from utils.browser import Browser
from utils.logger import logger
from utils.notify import Notification

def initialize_browser() -> Optional[Browser]:
    """Initialize browser with proper error handling"""
    try:
        return Browser()
    except Exception as e:
        logger.log_error_with_context(e, {
            "operation": "browser_initialization",
            "component": "main"
        })
        return None

def run_exam_check(browser: Browser) -> bool:
    """Main workflow for checking exam results"""
    start_time = datetime.now()
    try:
        # Login Process
        logger.info("Starting login process")
        login_page = LoginPage(browser)
        if not login_page.login():
            logger.info("Exiting due to alert notification")
            return False

        # Results Process
        logger.info("Starting results check process")
        results_page = ResultsPage(browser)
        results_page.navigate_to_results_page()
        
        # Get and process results
        logger.info("Retrieving exam results")
        new_results = results_page.get_results()

        # Notify if new results found
        if new_results:
            logger.info(f"Found {len(new_results)} new results, sending notifications")
            notification = Notification()
            notification.notify_new_results(new_results)
        else:
            logger.info("No new results found")

        return True

    except Exception as e:
        logger.log_error_with_context(e, {
            "operation": "exam_check",
            "component": "main"
        })
        return False
    finally:
        logger.log_operation_time("exam_check_total", start_time)

def main():
    """Main entry point of the application"""
    total_start_time = datetime.now()
    
    try:
        # Initialize browser
        browser = initialize_browser()
        if not browser:
            logger.error("Failed to initialize browser")
            sys.exit(1)

        # Run main workflow
        with browser:
            success = run_exam_check(browser)
            
        # Exit with appropriate status
        sys.exit(0 if success else 1)

    except Exception as e:
        logger.log_error_with_context(e, {
            "operation": "main",
            "component": "main"
        })
        sys.exit(1)
    finally:
        logger.log_operation_time("total_execution", total_start_time)

if __name__ == "__main__":
    main()