import sqlite3
from models.model import Result
from utils.logger import logger


class Database:
    def __init__(self):
        logger.info("Initializing database")
        self.conn = sqlite3.connect("data/results.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        logger.info("Creating table")
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS results (
                lesson_id TEXT,
                lesson_name TEXT,
                exam_type TEXT,
                score REAL
            )""")
        self.conn.commit()
    
    def insert_result(self, result: Result):
        logger.info("Inserting result")
        self.cursor.execute("""
            INSERT INTO results (lesson_id, lesson_name, exam_type, score)
            VALUES (?, ?, ?, ?)
        """, (result.lesson_id, result.lesson_name, result.exam_type, result.score))
        self.conn.commit()
    
    def check_if_result_exists(self, lesson_id: str, exam_type: str):
        logger.info("Checking if result exists")
        self.cursor.execute("""
            SELECT * FROM results WHERE lesson_id = ? AND exam_type = ?
        """, (lesson_id, exam_type))
        return self.cursor.fetchone() is not None
    
    