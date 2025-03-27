import sqlite3
from models.model import Result
from utils.logger import logger
from datetime import datetime
from typing import Optional, Tuple


class Database:
    def __init__(self):
        start_time = datetime.now()
        try:
            logger.info("Initializing database connection")
            self.db_path = "data/results.db"
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            logger.info(f"Connected to database: {self.db_path}")
            self.create_table()
        except sqlite3.Error as e:
            logger.log_error_with_context(e, {
                "operation": "database_init",
                "db_path": self.db_path
            })
            raise
        finally:
            logger.log_operation_time("database_init", start_time)

    def create_table(self):
        start_time = datetime.now()
        try:
            logger.info("Creating results table if not exists")
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    lesson_id TEXT,
                    lesson_name TEXT,
                    exam_type TEXT,
                    score REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.commit()
            logger.info("Table creation successful")
        except sqlite3.Error as e:
            logger.log_error_with_context(e, {
                "operation": "create_table",
                "table": "results"
            })
            raise
        finally:
            logger.log_operation_time("create_table", start_time)
    
    def insert_result(self, result: Result) -> bool:
        start_time = datetime.now()
        try:
            logger.info(f"Inserting result for {result.lesson_name} ({result.exam_type})")
            query = """
                INSERT INTO results (lesson_id, lesson_name, exam_type, score)
                VALUES (?, ?, ?, ?)
            """
            params = (result.lesson_id, result.lesson_name, result.exam_type, result.score)
            
            logger.log_request_response(
                "DB_INSERT",
                f"Query: {query.strip()}\nParams: {params}"
            )
            
            self.cursor.execute(query, params)
            self.conn.commit()
            
            logger.info(f"Successfully inserted result: {result.lesson_name} - {result.exam_type}")
            return True
        except sqlite3.Error as e:
            logger.log_error_with_context(e, {
                "operation": "insert_result",
                "result": str(result.__dict__),
                "query": query
            })
            return False
        finally:
            logger.log_operation_time("insert_result", start_time)
    
    def check_if_result_exists(self, lesson_id: str, exam_type: str) -> bool:
        start_time = datetime.now()
        try:
            logger.info(f"Checking existence of result: {lesson_id} ({exam_type})")
            query = """
                SELECT COUNT(*) FROM results 
                WHERE lesson_id = ? AND exam_type = ?
            """
            params = (lesson_id, exam_type)
            
            logger.log_request_response(
                "DB_CHECK",
                f"Query: {query.strip()}\nParams: {params}"
            )
            
            self.cursor.execute(query, params)
            count = self.cursor.fetchone()[0]
            
            exists = count > 0
            logger.info(f"Result exists: {exists}")
            return exists
        except sqlite3.Error as e:
            logger.log_error_with_context(e, {
                "operation": "check_result",
                "lesson_id": lesson_id,
                "exam_type": exam_type,
                "query": query
            })
            return False
        finally:
            logger.log_operation_time("check_result", start_time)

    def __del__(self):
        """Ensure proper cleanup of database connection"""
        try:
            if hasattr(self, 'conn'):
                self.conn.close()
                logger.info("Database connection closed")
        except sqlite3.Error as e:
            logger.log_error_with_context(e, {
                "operation": "database_cleanup"
            })
    
    