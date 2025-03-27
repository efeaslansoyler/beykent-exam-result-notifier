from selenium.webdriver.common.by import By
from utils.browser import Browser
from utils.logger import logger
from utils.database import Database
from models.model import Result
import time

class ResultsPage:
    def __init__(self, browser: Browser):
        self.browser = browser
        self.menu_button = (By.XPATH, "/html/body/form/div[6]/aside/div[2]/nav/span/ul/li[3]/a")
        self.results_page_button = (By.XPATH, "/html/body/form/div[6]/aside/div[2]/nav/span/ul/li[3]/ul/li[4]/a")
        self.database = Database()
    def navigate_to_results_page(self):
        logger.info("Navigating to results menu")
        self.browser.find_element(self.menu_button[0], self.menu_button[1]).click()
        self.browser.find_element(self.results_page_button[0], self.results_page_button[1]).click()
        
    def get_results(self):
        self.browser.switch_to_frame("IFRAME1")
        logger.info("Switched to frame")
        
        table = self.browser.find_element(By.XPATH, '//*[@id="grd_not_listesi"]')
        rows = table.find_elements(By.TAG_NAME, "tr")
        new_results = []

        for row in rows[1:]:
            cells = row.find_elements(By.TAG_NAME, "td")
            score_cell = cells[4]
            score_spans = score_cell.find_elements(By.TAG_NAME, "span")
            
            if not score_spans:
                logger.info("No exam results have been announced yet")
                return []

            lesson_id = cells[1].find_element(By.TAG_NAME, "span").text
            lesson_name = cells[2].text
            
            for span in score_spans:
                text = span.text.strip()
                if "Vize :" in text:
                    score = float(text.split(":")[1].strip())
                    if not self.database.check_if_result_exists(lesson_id, "midterm"):
                        new_results.append(Result(
                            lesson_id,
                            lesson_name,
                            exam_type="midterm",
                            score=score
                        ))
                elif "Final :" in text:
                    score = float(text.split(":")[1].strip())
                    if not self.database.check_if_result_exists(lesson_id, "final"):
                        new_results.append(Result(
                            lesson_id,
                            lesson_name,
                            exam_type="final",
                            score=score
                        ))
                elif "Büt :" in text:
                    score = float(text.split(":")[1].strip())
                    if not self.database.check_if_result_exists(lesson_id, "make-up"):
                        new_results.append(Result(
                            lesson_id,
                            lesson_name,
                            exam_type="make-up",
                            score=score
                        ))
        for result in new_results:
            self.database.insert_result(result)

        return new_results
    
    