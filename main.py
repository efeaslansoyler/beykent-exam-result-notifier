from pages.login_page import LoginPage
from utils.browser import Browser
from utils.logger import logger

def main():
    browser = Browser()  # Create browser without context manager
    try:
        login_page = LoginPage(browser)
        login_page.login()
        input("Press Enter to close the browser...")  # Wait for user input on success
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        input("Press Enter to close the browser...")  # Wait for user input on error
    browser.quit()  # Only quit after user input in both cases

if __name__ == "__main__":
    main()