from selenium.webdriver.common.by import By
from utils.browser import Browser
from utils.config import get_env_var
from utils.logger import logger

class ResultsPage:
    def __init__(self, browser: Browser):
        self.browser = browser
        self.menu_button = (By.XPATH, "/html/body/form/div[6]/aside/div[2]/nav/span/ul/li[3]/a")
        self.results_page_button = (By.XPATH, "/html/body/form/div[6]/aside/div[2]/nav/span/ul/li[3]/ul/li[4]/a")
    
    def navigate_to_results_page(self):
        logger.info("Navigating to results page")
        self.browser.find_element(self.menu_button[0], self.menu_button[1]).click()
        self.browser.find_element(self.results_page_button[0], self.results_page_button[1]).click()