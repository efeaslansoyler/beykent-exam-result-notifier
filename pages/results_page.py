from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from utils.browser import Browser
from utils.logger import logger
from utils.database import Database
from models.model import Result
from typing import List
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

class ResultsPage:
    def __init__(self, browser: Browser):
        self.browser = browser
        self.database = Database()
        
        # Locators
        self.menu_button = (By.XPATH, "/html/body/form/div[6]/aside/div[2]/nav/span/ul/li[3]/a")
        self.results_page_button = (By.XPATH, "/html/body/form/div[6]/aside/div[2]/nav/span/ul/li[3]/ul/li[4]/a")
        self.results_table = (By.XPATH, '//*[@id="grd_not_listesi"]')
        self.results_frame = "IFRAME1"
        
    def navigate_to_results_page(self) -> None:
        """Navigate to the results page through the menu"""
        start_time = datetime.now()
        try:
            logger.info("Navigating to results menu")
            self.browser.find_element(*self.menu_button).click()
            self.browser.find_element(*self.results_page_button).click()
        except Exception as e:
            logger.log_error_with_context(e, {
                "operation": "navigate_to_results_page",
                "menu_button": self.menu_button,
                "results_button": self.results_page_button
            })
            raise
        finally:
            logger.log_operation_time("navigate_to_results", start_time)
        
    def switch_to_results_frame(self) -> None:
        """Switch to the frame containing results"""
        logger.info("Switching to results frame")
        self.browser.switch_to_frame(self.results_frame)
        
    def extract_lesson_info(self, row) -> tuple[str, str]:
        """
        Extract lesson ID and name from a table row
        
        Args:
            row: The table row element
            
        Returns:
            tuple: (lesson_id, lesson_name)
        """
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            lesson_id = cells[1].find_element(By.TAG_NAME, "span").text
            lesson_name = cells[2].text
            return lesson_id, lesson_name
        except (IndexError, NoSuchElementException) as e:
            logger.error(f"Error extracting lesson info: {e}")
            raise
            
    def parse_score_cell(self, score_cell) -> List[Result]:
        """
        Parse the score cell and extract exam results
        
        Args:
            score_cell: The cell containing exam scores
            
        Returns:
            List[Result]: List of new results found
        """
        results = []
        score_spans = score_cell.find_elements(By.TAG_NAME, "span")
        
        if not score_spans:
            logger.info("No exam results found in cell")
            return results
            
        for span in score_spans:
            text = span.text.strip()
            for exam_type, keyword in [
                ("midterm", "Vize :"),
                ("final", "Final :"),
                ("make-up", "Büt :")
            ]:
                if keyword in text:
                    score = float(text.split(":")[1].strip())
                    if not self.database.check_if_result_exists(self.current_lesson_id, exam_type):
                        results.append(Result(
                            self.current_lesson_id,
                            self.current_lesson_name,
                            exam_type=exam_type,
                            score=score
                        ))
        return results
        
    def process_results_table(self) -> List[Result]:
        """Process the results table and extract all new results"""
        start_time = datetime.now()
        try:
            table = self.browser.find_element(By.XPATH, '//*[@id="grd_not_listesi"]')
            rows = table.find_elements(By.TAG_NAME, "tr")
            new_results = []
            
            # Add row count info
            logger.info(f"Processing {len(rows)-1} rows from results table")
            
            # Skip header row
            for row_index, row in enumerate(rows[1:], 1):
                try:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) < 5:
                        continue
                        
                    lesson_id = cells[1].find_element(By.TAG_NAME, "span").text
                    lesson_name = cells[2].text
                    score_text = cells[4].text
                    
                    logger.info(f"Processing row {row_index}: {lesson_name}")
                    
                    # Process all exam types in one pass
                    for exam_info in [
                        ("Vize :", "midterm"),
                        ("Final :", "final"),
                        ("Büt :", "make-up")
                    ]:
                        identifier, exam_type = exam_info
                        if identifier in score_text:
                            try:
                                score = float(score_text.split(identifier)[1].split()[0])
                                if not self.database.check_if_result_exists(lesson_id, exam_type):
                                    new_results.append(Result(lesson_id, lesson_name, exam_type, score))
                                    logger.info(f"New {exam_type} result found for {lesson_name}: {score}")
                            except (ValueError, IndexError):
                                continue
                                
                except Exception as e:
                    logger.log_error_with_context(e, {
                        "operation": "process_row",
                        "row_index": row_index,
                        "lesson_name": lesson_name if 'lesson_name' in locals() else "unknown"
                    })
                    continue
                    
            logger.info(f"Found {len(new_results)} new results")
            return new_results
            
        except Exception as e:
            logger.log_error_with_context(e, {
                "operation": "process_results_table"
            })
            raise
        finally:
            logger.log_operation_time("process_results_table", start_time)
        
    def save_results(self, results: List[Result]) -> None:
        """Save new results to database"""
        start_time = datetime.now()
        try:
            for result in results:
                try:
                    self.database.insert_result(result)
                    logger.log_request_response("DB_INSERT", f"Saved result: {result.lesson_name} - {result.exam_type}")
                except Exception as e:
                    logger.log_error_with_context(e, {
                        "operation": "save_result",
                        "result": str(result)
                    })
        finally:
            logger.log_operation_time("save_results", start_time)
                
    def get_results(self) -> List[Result]:
        """Main method to get all new results"""
        start_time = datetime.now()
        try:
            self.browser.switch_to_frame(self.results_frame)
            logger.info("Switched to frame")
            
            new_results = self.process_results_table()
            if new_results:
                logger.info(f"Found {len(new_results)} new results")
                self.save_results(new_results)
            
            return new_results
            
        except Exception as e:
            logger.log_error_with_context(e, {
                "operation": "get_results"
            })
            raise
        finally:
            try:
                self.browser.switch_to_default_content()
            except Exception as e:
                logger.log_error_with_context(e, {
                    "operation": "switch_to_default_content"
                })
            logger.log_operation_time("get_results", start_time)
    
    