from selenium.webdriver.common.by import By
from utils.browser import Browser
from utils.config import get_env_var
from utils.captcha_solver import CaptchaSolver
from utils.logger import logger
import time

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
        logger.info("Navigating to login page")
        self.browser.go_to_url(self.login_url)

    def enter_username(self):
        logger.info("Entering username")
        self.browser.enter_text(self.username_input[0], self.username_input[1], self.username)

    def enter_password(self):
        logger.info("Entering password")
        self.browser.enter_text(self.password_input[0], self.password_input[1], self.password)

    def get_captcha_image(self):
        logger.info("Getting captcha image")
        self.browser.take_screenshot_element(self.captcha_image[0], self.captcha_image[1], filename="captcha.png")

    def calculate_captcha(self):
        logger.info("Calculating captcha")
        solver = CaptchaSolver("data/captcha.png")
        result = solver.solve_captcha()
        logger.info(f"Captcha solution: {result}")
        self.browser.enter_text(self.captcha_input[0], self.captcha_input[1], result)

    def click_login_button(self):
        logger.info("Clicking login button")
        self.browser.click_element(self.login_button[0], self.login_button[1])

    def check_login_success(self):
        logger.info("Checking login success")
        logger.info(f"Current URL: {self.browser.get_current_url()}")
        try:
            return self.browser.get_current_url() == self.home_url
        except Exception as e:
            logger.error(f"Error checking login success: {e}")
            return False
    
    def login(self):
        max_attempts = 3  # Increased from 2 to 3 attempts
        attempt = 1
        
        while attempt <= max_attempts:
            try:
                logger.info(f"Login attempt {attempt}/{max_attempts}")
                self.navigate_to_login_page()
                self.enter_username()
                self.enter_password()
                self.get_captcha_image()
                self.calculate_captcha()
                self.click_login_button()
                if self.check_login_success():  
                    logger.info("Login successful")
                    return  # Exit the function if login is successful
                logger.warning("Login unsuccessful, URL does not match expected home URL")
                # Increment attempt if login was not successful
                attempt += 1
            except Exception as e:
                logger.error(f"Login attempt {attempt} failed: {e}")
                if attempt < max_attempts:
                    logger.info("Retrying login...")
                    time.sleep(3)  # Add delay before retry
                    attempt += 1
                else:
                    logger.error("Max login attempts reached")
                    raise  # Re-raise the exception after all attempts fail
