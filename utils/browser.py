from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from utils.logger import logger
from utils.config import get_env_var
import os


class Browser:
    def __init__(self):
        try:
            logger.info("Initializing browser...")
            self.options = Options()
            self.headless = get_env_var("HEADLESS")
            self.screenshot_folder = get_env_var("SCREENSHOTS_FOLDER")
            if self.headless: 
                self.options.add_argument("--headless")
            self.driver = webdriver.Firefox(options=self.options)
        except Exception as e:
            logger.error(f"Error initializing browser: {e}")
            raise

    def __enter__(self) -> 'Browser':
        """
        Context manager entry point.
        
        Returns:
            Browser: The browser instance
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Context manager exit point.
        Ensures the browser is properly closed even if an exception occurs.
        
        Args:
            exc_type: The type of the exception that occurred, if any
            exc_val: The exception instance that occurred, if any
            exc_tb: The traceback of the exception that occurred, if any
        """
        self.quit()

    def go_to_url(self, url: str) -> None:
        """
        Navigate to the specified URL.
        
        Args:
            url (str): The URL to navigate to
        """
        try:
            logger.info(f"Navigating to URL: {url}")
            self.driver.get(url)
        except Exception as e:
            logger.error(f"Error navigating to URL {url}: {e}")
            raise
    
    def find_element(self, by: By, value: str, timeout: int = 10) -> WebElement:
        """
        Find an element in the DOM.
        
        Args:
            by (By): The method to use to find the element
            value (str): The value to use to find the element
            timeout (int): The timeout for the wait
            
        Returns:
            WebElement: The found element
            
        Raises:
            TimeoutException: If the element is not found within the timeout period
        """
        try:
            logger.info(f"Finding element: {by}={value}")
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except Exception as e:
            logger.error(f"Error finding element {by}={value}: {e}")
            raise
    
    def click_element(self, by: By, value: str, timeout: int = 10) -> None:
        """
        Wait for an element to be clickable and click it.
        
        Args:
            by (By): The method to locate the element
            value (str): The value to search for
            timeout (int): Maximum time to wait in seconds
        """
        try:
            logger.info(f"Clicking element: {by}={value}")
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
        except Exception as e:
            logger.error(f"Error clicking element {by}={value}: {e}")
            raise

    def get_text(self, by: By, value: str, timeout: int = 10) -> str:
        """
        Get text from an element after waiting for it to be present.
        
        Args:
            by (By): The method to locate the element
            value (str): The value to search for
            timeout (int): Maximum time to wait in seconds
            
        Returns:
            str: The text content of the element
        """
        try:
            logger.info(f"Getting text from element: {by}={value}")
            element = self.find_element(by, value, timeout)
            return element.text
        except Exception as e:
            logger.error(f"Error getting text from element {by}={value}: {e}")
            raise

    def enter_text(self, by: By, value: str, text: str, timeout: int = 10) -> None:
        """
        Enter text into an input element.
        
        Args:
            by (By): The method to locate the element
            value (str): The value to search for
            text (str): The text to enter
            timeout (int): Maximum time to wait in seconds
        """
        try:
            logger.info(f"Entering text into element: {by}={value}")
            element = self.find_element(by, value, timeout)
            element.clear()  # Clear existing text first
            element.send_keys(text)
        except Exception as e:
            logger.error(f"Error entering text into element {by}={value}: {e}")
            raise
    
    def find_elements(self, by: By, value: str, timeout: int = 10) -> list[WebElement]:
        """
        Find all elements matching the selector.
        
        Args:
            by (By): The method to locate the elements
            value (str): The value to search for
            timeout (int): Maximum time to wait in seconds
            
        Returns:
            list[WebElement]: List of found elements
        """
        try:
            logger.info(f"Finding elements: {by}={value}")
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((by, value))
            )
            return elements
        except Exception as e:
            logger.error(f"Error finding elements {by}={value}: {e}")
            raise
    
    def take_screenshot_element(self, by: By, value: str, timeout: int = 10, filename: str = "screenshot.png") -> None:
        """
        Take a screenshot of the element.
        
        Args:
            by (By): The method to locate the element
            value (str): The value to search for
            timeout (int): Maximum time to wait in seconds
            filename (str): The filename to save the screenshot to
        """

        if not os.path.exists(self.screenshot_folder):
            os.makedirs(self.screenshot_folder)
        
        filepath = os.path.join(self.screenshot_folder, filename)

        try:
            logger.info(f"Taking screenshot: {filepath}")
            element = self.find_element(by, value, timeout)
            
            # Remove height and width constraints using JavaScript
            self.driver.execute_script("""
                arguments[0].style.height = 'auto';
                arguments[0].style.width = 'auto';
            """, element)
            
            # Take the screenshot
            element.screenshot(filepath)
            
        except Exception as e:
            logger.error(f"Error taking screenshot {filename}: {e}")
            raise

    def get_current_url(self) -> str:
        """
        Get the current URL of the browser.
        
        Returns:
            str: The current URL
        """
        try:
            logger.info("Getting current URL")
            return self.driver.current_url
        except Exception as e:
            logger.error(f"Error getting current URL: {e}")
            raise

    def quit(self) -> None:
        """
        Properly close the browser and clean up resources.
        """
        try:
            logger.info("Closing browser...")
            self.driver.quit()
        except Exception as e:
            logger.error(f"Error closing browser: {e}")
            raise
