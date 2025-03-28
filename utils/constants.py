from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os

load_dotenv()

# Username and password for Beykent OBS system
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Browser settings
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"

# NTFY.SH settings
NTFY_TOPIC = os.getenv("NTFY_TOPIC")

# Base URLs for Beykent OBS system
LOGIN_URL = "https://obs.beykent.edu.tr/oibs/std/login.aspx"
HOME_URL = "https://obs.beykent.edu.tr/oibs/std/index.aspx?curOp=0"

# Folder paths
DATA_FOLDER = "data"
LOGS_FOLDER = "logs"
SCREENSHOTS_FOLDER = "data/screenshots"

# Login page locators
LOGIN_PAGE_LOCATORS = {
    "username_input": (By.ID, "txtParamT01"),
    "password_input": (By.ID, "txtParamT02"),
    "captcha_image": (By.ID, "imgCaptchaImg"),
    "captcha_input": (By.ID, "txtSecCode"),
    "login_button": (By.ID, "btnLogin")
}

# Results page locators
RESULTS_PAGE_LOCATORS = {
    "menu_button": (By.XPATH, "/html/body/form/div[6]/aside/div[2]/nav/span/ul/li[3]/a"),
    "results_page_button": (By.XPATH, "/html/body/form/div[6]/aside/div[2]/nav/span/ul/li[3]/ul/li[4]/a"),
    "results_table": (By.XPATH, '//*[@id="grd_not_listesi"]'),
    "results_frame": "IFRAME1"
}






