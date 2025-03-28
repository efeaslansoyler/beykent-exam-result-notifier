from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.browser import Browser
from utils.captcha_solver import CaptchaSolver
from utils.logger import logger
from utils.notify import Notification
from datetime import datetime
from selenium.common.exceptions import (TimeoutException,WebDriverException)
from utils.constants import USERNAME, PASSWORD, LOGIN_URL, HOME_URL, LOGIN_PAGE_LOCATORS
import time

class LoginPage:
    def __init__(self, browser: Browser):
        self.browser = browser

        self.username = USERNAME
        self.password = PASSWORD
        self.login_url = LOGIN_URL
        self.home_url = HOME_URL
        
        # Locators
        self.username_input = LOGIN_PAGE_LOCATORS["username_input"]
        self.password_input = LOGIN_PAGE_LOCATORS["password_input"]
        self.captcha_image = LOGIN_PAGE_LOCATORS["captcha_image"]
        self.captcha_input = LOGIN_PAGE_LOCATORS["captcha_input"]
        self.login_button = LOGIN_PAGE_LOCATORS["login_button"]

    def navigate_to_login_page(self):
        start_time = datetime.now()
        try:
            logger.info("Navigating to login page")
            self.browser.driver.set_page_load_timeout(5)
            self.browser.go_to_url(self.login_url)
            wait = WebDriverWait(self.browser.driver, 3)
            wait.until(
                EC.presence_of_element_located(self.username_input)
            )
            return True
        except TimeoutException:
            logger.log_error_with_context(TimeoutException(f"Timeout while navigating to {self.login_url}"), {
                "operation": "navigate_to_login",
                "url": self.login_url
            })
            return False
        except WebDriverException as e:
            logger.log_error_with_context(e, {
                "operation": "navigate_to_login",
                "url": self.login_url
            })
            return False
        finally:
            logger.log_operation_time("navigate_to_login", start_time)

    def enter_username(self):
        start_time = datetime.now()
        try:
            logger.info("Entering username")
            self.browser.enter_text(self.username_input[0], self.username_input[1], self.username)
            return True
        except Exception as e:
            logger.log_error_with_context(e, {
                "operation": "enter_username",
                "field": self.username_input
            })
            return False
        finally:
            logger.log_operation_time("enter_username", start_time)

    def enter_password(self):
        start_time = datetime.now()
        try:
            logger.info("Entering password")
            self.browser.enter_text(self.password_input[0], self.password_input[1], self.password)
            return True
        except Exception as e:
            logger.log_error_with_context(e, {
                "operation": "enter_password",
                "field": self.password_input
            })
            return False
        finally:
            logger.log_operation_time("enter_password", start_time)

    def get_captcha_image(self):
        start_time = datetime.now()
        try:
            logger.info("Getting captcha image")
            self.browser.take_screenshot_element(self.captcha_image[0], self.captcha_image[1], filename="captcha.png")
            return True
        except Exception as e:
            logger.log_error_with_context(e, {
                "operation": "get_captcha_image",
                "element": self.captcha_image
            })
            return False
        finally:
            logger.log_operation_time("get_captcha_image", start_time)

    def calculate_captcha(self):
        start_time = datetime.now()
        try:
            logger.info("Calculating captcha")
            solver = CaptchaSolver("data/screenshots/captcha.png")
            result = solver.solve_captcha()
            logger.info(f"Captcha solution: {result}")
            self.browser.enter_text(self.captcha_input[0], self.captcha_input[1], result)
            return True
        except Exception as e:
            logger.log_error_with_context(e, {
                "operation": "calculate_captcha",
                "input_field": self.captcha_input
            })
            return False
        finally:
            logger.log_operation_time("calculate_captcha", start_time)

    def click_login_button(self):
        start_time = datetime.now()
        try:
            logger.info("Clicking login button")
            wait = WebDriverWait(self.browser.driver, 3)
            button = wait.until(
                EC.element_to_be_clickable(self.login_button)
            )
            button.click()
            return True
        except Exception as e:
            logger.log_error_with_context(e, {
                "operation": "click_login_button",
                "button": self.login_button
            })
            return False
        finally:
            logger.log_operation_time("click_login_button", start_time)

    def check_home_url(self):
        start_time = datetime.now()
        try:
            logger.info("Checking if redirected to home page")
            current_url = self.browser.get_current_url()
            logger.info(f"Current URL: {current_url}")
            if current_url == self.home_url:
                return True
            logger.log_error_with_context(Exception("URL mismatch"), {
                "operation": "check_home_url",
                "expected": self.home_url,
                "actual": current_url
            })
            return False
        finally:
            logger.log_operation_time("check_home_url", start_time)

    def check_alert(self):
        start_time = datetime.now()
        try:
            logger.info("Checking alert")
            self.browser.switch_to_frame("IFRAME1")
            try:
                original_timeout = self.browser.driver.timeouts.implicit_wait
                self.browser.driver.implicitly_wait(0)
                
                try:
                    wait = WebDriverWait(self.browser.driver, 2, poll_frequency=0.2)
                    alert = wait.until(
                        EC.presence_of_element_located((By.ID, "divRequired"))
                    )
                    notification = Notification()
                    notification.send_alert("Lütfen iletişim bilgilerinizi güncelleyiniz. Güncellemediğiniz takdirde ileti sistemi çalışmayacaktır.")
                    logger.info("Contact information update alert detected and notification sent")
                    return True
                except TimeoutException:
                    logger.info("No contact information alert found")
                    return False
                finally:
                    self.browser.driver.implicitly_wait(original_timeout)
            finally:
                self.browser.switch_to_default_content()
        except Exception as e:
            logger.log_error_with_context(e, {
                "operation": "check_alert",
                "frame": "IFRAME1"
            })
            return False
        finally:
            logger.log_operation_time("check_alert", start_time)

    def login(self):
        start_time = datetime.now()
        max_attempts = 3
        attempt = 1
        
        while attempt <= max_attempts:
            logger.info(f"Login attempt {attempt}/{max_attempts}")
            
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
                if self.check_alert():
                    logger.info("Alert found - exiting after notification")
                    return False
                logger.info("Login successful")
                logger.log_operation_time("login_total", start_time)
                return True
                
            if attempt > max_attempts:
                logger.error("Max login attempts reached")
                raise Exception("Failed to login after maximum attempts")
            
        return False
