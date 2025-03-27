from pages.login_page import LoginPage
from pages.results_page import ResultsPage
from utils.browser import Browser
from utils.logger import logger
from utils.notify import Notification

def main():
    with Browser() as browser:
        try:
            logger.info("Starting browser")
            login_page = LoginPage(browser)

            logger.info("Logging in")
            if not login_page.login():
                logger.info("Exiting due to alert notification")
                return

            logger.info("Navigating to results page")
            results_page = ResultsPage(browser)
            results_page.navigate_to_results_page()

            logger.info("Getting results")
            new_results = results_page.get_results()

            logger.info("Notifying new results")
            notification = Notification()
            notification.notify_new_results(new_results)
            
        except Exception as e:
            logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()