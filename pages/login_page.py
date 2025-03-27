from selenium.webdriver.common.by import By
from utils.browser import Browser
from utils.config import get_env_var
from utils.captcha_solver import CaptchaSolver
from utils.logger import logger
from utils.notify import Notification
import time
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementNotInteractableException,
    WebDriverException
)

class LoginPage:
    def __init__(self, browser: Browser):
        self.browser = browser
        self.username = get_env_var("USERNAME")
        self.password = get_env_var("PASSWORD")
        self.login_url = get_env_var("LOGIN_URL")
        self.home_url = get_env_var("HOME_URL")
        self.username_input = (By.ID, "txtParamT01")
        self.password_input = (By.ID, "txtParamT02")
        self.captcha_image = (By.ID, "imgCaptchaImg")
        self.captcha_input = (By.ID, "txtSecCode")
        self.login_button = (By.ID, "btnLogin")

    def navigate_to_login_page(self):
        try:
            logger.info("Navigating to login page")
            self.browser.go_to_url(self.login_url)
            return True
        except TimeoutException:
            logger.error(f"Timeout while navigating to {self.login_url}")
            return False
        except WebDriverException as e:
            logger.error(f"Failed to navigate to login page: {str(e)}")
            return False

    def enter_username(self):
        try:
            logger.info("Entering username")
            self.browser.enter_text(self.username_input[0], self.username_input[1], self.username)
            return True
        except NoSuchElementException:
            logger.error("Username input field not found")
            return False
        except ElementNotInteractableException:
            logger.error("Username input field not interactable")
            return False
        except Exception as e:
            logger.error(f"Failed to enter username: {str(e)}")
            return False

    def enter_password(self):
        try:
            logger.info("Entering password")
            self.browser.enter_text(self.password_input[0], self.password_input[1], self.password)
            return True
        except NoSuchElementException:
            logger.error("Password input field not found")
            return False
        except ElementNotInteractableException:
            logger.error("Password input field not interactable")
            return False
        except Exception as e:
            logger.error(f"Failed to enter password: {str(e)}")
            return False

    def get_captcha_image(self):
        try:
            logger.info("Getting captcha image")
            self.browser.take_screenshot_element(self.captcha_image[0], self.captcha_image[1], filename="captcha.png")
            return True
        except NoSuchElementException:
            logger.error("Captcha image element not found")
            return False
        except Exception as e:
            logger.error(f"Failed to capture captcha image: {str(e)}")
            return False

    def calculate_captcha(self):
        try:
            logger.info("Calculating captcha")
            solver = CaptchaSolver("data/screenshots/captcha.png")
            result = solver.solve_captcha()
            logger.info(f"Captcha solution: {result}")
            self.browser.enter_text(self.captcha_input[0], self.captcha_input[1], result)
            return True
        except FileNotFoundError:
            logger.error("Captcha image file not found")
            return False
        except NoSuchElementException:
            logger.error("Captcha input field not found")
            return False
        except Exception as e:
            logger.error(f"Failed to solve or enter captcha: {str(e)}")
            return False

    def click_login_button(self):
        try:
            logger.info("Clicking login button")
            self.browser.click_element(self.login_button[0], self.login_button[1])
            return True
        except NoSuchElementException:
            logger.error("Login button not found")
            return False
        except ElementNotInteractableException:
            logger.error("Login button not clickable")
            return False
        except Exception as e:
            logger.error(f"Failed to click login button: {str(e)}")
            return False

    def check_home_url(self):
        try:
            logger.info("Checking if redirected to home page")
            current_url = self.browser.get_current_url()
            logger.info(f"Current URL: {current_url}")
            if current_url == self.home_url:
                return True
            logger.error(f"Current URL '{current_url}' does not match expected home URL '{self.home_url}'")
            return False
        except Exception as e:
            logger.error(f"Error checking home URL: {str(e)}")
            return False

    def check_alert(self):
        try:
            logger.info("Checking alert")
            self.browser.switch_to_frame("IFRAME1")
            try:
                alert = self.browser.driver.find_element(By.ID, "divRequired")
                notification = Notification()
                notification.send_alert("Lütfen iletişim bilgilerinizi güncelleyiniz. Güncellemediğiniz takdirde ileti sistemi çalışmayacaktır.")
                logger.info("Contact information update alert detected and notification sent")
                return True
            except NoSuchElementException:
                logger.info("No contact information alert found")
                return False
            finally:
                self.browser.switch_to_default_content()
        except Exception as e:
            logger.error(f"Error checking for alert: {str(e)}")
            return False

    def login(self):
        max_attempts = 3
        attempt = 1
        
        while attempt <= max_attempts:
            logger.info(f"Login attempt {attempt}/{max_attempts}")
            
            # Execute each step and check for failures
            steps = [
                self.navigate_to_login_page,
                self.enter_username,
                self.enter_password,
                self.get_captcha_image,
                self.calculate_captcha,
                self.click_login_button,
                self.check_home_url
            ]
            
            for step in steps:
                if not step():
                    logger.warning(f"Step '{step.__name__}' failed, retrying login process")
                    attempt += 1
                    time.sleep(3)
                    break
            else:
                # All steps succeeded, now check for alert
                if self.check_alert():
                    logger.info("Alert found - exiting after notification")
                    return False
                logger.info("Login successful")
                return True
                
            if attempt > max_attempts:
                logger.error("Max login attempts reached")
                raise Exception("Failed to login after maximum attempts")
            
        return False
