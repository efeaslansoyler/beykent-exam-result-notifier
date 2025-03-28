from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from utils.logger import logger
from datetime import datetime
import os
from utils.constants import HEADLESS, SCREENSHOTS_FOLDER

class Browser:
    def __init__(self):
        try:
            start_time = datetime.now()
            logger.info("Initializing browser...")
            
            self.options = Options()
            self.headless = HEADLESS
            self.screenshot_folder = SCREENSHOTS_FOLDER
            
            # Performance optimizations
            self.options.set_preference("browser.cache.disk.enable", False)
            self.options.set_preference("browser.cache.memory.enable", True)
            self.options.set_preference("browser.cache.offline.enable", False)
            self.options.set_preference("network.http.pipelining", True)
            self.options.set_preference("network.http.proxy.pipelining", True)
            self.options.set_preference("network.http.pipelining.maxrequests", 8)
            self.options.set_preference("content.notify.interval", 500000)
            self.options.set_preference("content.notify.ontimer", True)
            self.options.set_preference("content.switch.threshold", 250000)
            self.options.set_preference("browser.download.manager.scanWhenDone", False)
            self.options.set_preference("browser.sessionstore.interval", 1800000)
            
            # Disable unnecessary features
            self.options.set_preference("app.update.enabled", False)
            self.options.set_preference("browser.search.update", False)
            self.options.set_preference("extensions.update.enabled", False)
            
            if self.headless:
                self.options.add_argument("--headless")
                
            self.driver = webdriver.Firefox(options=self.options)
            logger.log_operation_time("browser_initialization", start_time)
            
            # Set page load strategy
            self.driver.set_page_load_timeout(30)
            self.driver.implicitly_wait(10)
            
        except Exception as e:
            logger.log_error_with_context(e, {
                "operation": "browser_init",
                "headless": self.headless
            })
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
        start_time = datetime.now()
        try:
            logger.log_request_response("FIND_ELEMENT", f"{by}={value}")
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except Exception as e:
            logger.log_error_with_context(e, {
                "operation": "find_element",
                "by": by,
                "value": value,
                "timeout": timeout
            })
            raise
        finally:
            logger.log_operation_time("find_element", start_time)

    def click_element(self, by: By, value: str, timeout: int = 10) -> None:
        """
        Wait for an element to be clickable and click it.
        
        Args:
            by (By): The method to locate the element
            value (str): The value to search for
            timeout (int): Maximum time to wait in seconds
        """
        start_time = datetime.now()
        try:
            logger.log_request_response("CLICK_ELEMENT", f"{by}={value}")
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
        except Exception as e:
            logger.log_error_with_context(e, {
                "operation": "click_element",
                "by": by,
                "value": value
            })
            raise
        finally:
            logger.log_operation_time("click_element", start_time)

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
        start_time = datetime.now()
        try:
            logger.log_request_response("ENTER_TEXT", f"Element: {by}={value}")
            element = self.find_element(by, value, timeout)
            element.clear()  # Clear existing text first
            element.send_keys(text)
        except Exception as e:
            logger.log_error_with_context(e, {
                "operation": "enter_text",
                "by": by,
                "value": value,
                "text_length": len(text)
            })
            raise
        finally:
            logger.log_operation_time("enter_text", start_time)
    
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

    def switch_to_frame(self, frame: str):
        """
        Switch to the frame.
        """
        start_time = datetime.now()
        try:
            logger.log_request_response("SWITCH_FRAME", f"Frame: {frame}")
            self.driver.switch_to.frame(frame)
        except Exception as e:
            logger.log_error_with_context(e, {
                "operation": "switch_frame",
                "frame": frame
            })
            raise
        finally:
            logger.log_operation_time("switch_frame", start_time)

    def switch_to_default_content(self):
        """
        Switch to the default content.
        """
        start_time = datetime.now()
        try:
            logger.log_request_response("SWITCH_DEFAULT", "Switching to default content")
            self.driver.switch_to.default_content()
        except Exception as e:
            logger.log_error_with_context(e, {
                "operation": "switch_default_content"
            })
            raise
        finally:
            logger.log_operation_time("switch_default_content", start_time)

    def quit(self) -> None:
        """
        Properly close the browser and clean up resources.
        """
        start_time = datetime.now()
        try:
            logger.info("Closing browser...")
            self.driver.quit()
        except Exception as e:
            logger.log_error_with_context(e, {
                "operation": "browser_quit"
            })
            raise
        finally:
            logger.log_operation_time("browser_quit", start_time)
