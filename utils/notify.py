import aiohttp
import asyncio
from utils.logger import logger
from pages.results_page import Result
from datetime import datetime
from typing import List
import platform
from utils.constants import NTFY_TOPIC

class Notification:
    def __init__(self):
        start_time = datetime.now()
        try:
            logger.info("Initializing Notification system")
            self.topic = NTFY_TOPIC
            if not self.topic:
                raise ValueError("TOPIC environment variable not set")
            self.base_url = f"https://ntfy.sh/{self.topic}"
            logger.info(f"Notification configured - URL: {self.base_url}")
        except Exception as e:
            logger.log_error_with_context(e, {
                "operation": "notification_init",
                "topic": self.topic if hasattr(self, 'topic') else None,
                "base_url": self.base_url if hasattr(self, 'base_url') else None
            })
            raise
        finally:
            logger.log_operation_time("notification_init", start_time)

    async def send_notification_async(self, session: aiohttp.ClientSession, result: Result) -> None:
        start_time = datetime.now()
        try:
            message = f"Sınav sonucunuz açıklandı!\n\nDers: {result.lesson_name}\nSınav: {result.exam_type}\nNot: {result.score}"
            headers = {
                "Title": "Beykent Universitesi Sinav Sonucunuz Aciklandi !",
                "Tags": "loudspeaker",
                "Priority": "high"
            }

            logger.info(f"Sending exam result notification for {result.lesson_name} ({result.exam_type})")
            logger.log_request_response(
                "NTFY_RESULT_REQUEST",
                f"URL: {self.base_url}\nHeaders: {headers}\nMessage: {message}"
            )

            async with session.post(
                self.base_url,
                data=message.encode("utf-8"),
                headers=headers,
                timeout=5
            ) as response:
                await response.text()
                response.raise_for_status()
                
                logger.info(f"Notification sent successfully for {result.lesson_name} {result.exam_type} with score {result.score}")
                logger.log_request_response(
                    "NTFY_RESULT_RESPONSE",
                    f"Status: {response.status}\nTime: {datetime.now() - start_time}"
                )
                
        except asyncio.TimeoutError:
            logger.log_error_with_context(Exception("Notification timeout"), {
                "operation": "send_notification",
                "result": str(result.__dict__),
                "timeout": "5 seconds"
            })
        except Exception as e:
            logger.log_error_with_context(e, {
                "operation": "send_notification",
                "result": str(result.__dict__),
                "url": self.base_url
            })
        finally:
            logger.log_operation_time("send_notification", start_time)

    async def send_alert_async(self, session: aiohttp.ClientSession, message: str) -> None:
        start_time = datetime.now()
        try:
            headers = {
                "Title": "beykent universitesi iletisim bilgilerinizi guncelleyiniz",
                "Tags": "warning",
                "Priority": "high"
            }
            
            logger.info(f"Sending alert notification")
            logger.log_request_response(
                "NTFY_ALERT_REQUEST",
                f"URL: {self.base_url}\nHeaders: {headers}\nMessage: {message}"
            )
            
            async with session.post(
                self.base_url,
                data=message.encode("utf-8"),
                headers=headers,
                timeout=5
            ) as response:
                await response.text()
                response.raise_for_status()
                
                logger.info(f"Alert sent successfully")
                logger.log_request_response(
                    "NTFY_ALERT_RESPONSE",
                    f"Status: {response.status}\nTime: {datetime.now() - start_time}"
                )
                
        except asyncio.TimeoutError:
            logger.log_error_with_context(Exception("Alert notification timeout"), {
                "operation": "send_alert",
                "timeout": "5 seconds"
            })
        except Exception as e:
            logger.log_error_with_context(e, {
                "operation": "send_alert",
                "url": self.base_url,
                "message": message
            })
        finally:
            logger.log_operation_time("send_alert", start_time)

    def send_alert(self, message: str) -> None:
        start_time = datetime.now()
        try:
            async def run_async():
                async with aiohttp.ClientSession() as session:
                    await self.send_alert_async(session, message)
            
            if platform.system() == 'Windows':
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            asyncio.run(run_async())
            
        except Exception as e:
            logger.log_error_with_context(e, {
                "operation": "send_alert",
                "message": message
            })
        finally:
            logger.log_operation_time("send_alert", start_time)

    def notify_new_results(self, results: List[Result]) -> None:
        start_time = datetime.now()
        try:
            if not results:
                logger.info("No new results to notify")
                return

            total_results = len(results)
            logger.info(f"Preparing to send notifications for {total_results} new results")
            
            async def send_all_notifications():
                async with aiohttp.ClientSession() as session:
                    tasks = []
                    for index, result in enumerate(results, 1):
                        logger.info(f"Processing notification {index}/{total_results}")
                        task = asyncio.create_task(self.send_notification_async(session, result))
                        tasks.append(task)
                    await asyncio.gather(*tasks)

            if platform.system() == 'Windows':
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            asyncio.run(send_all_notifications())
            
            logger.info(f"Successfully sent notifications for {total_results} results")
        except Exception as e:
            logger.log_error_with_context(e, {
                "operation": "notify_new_results",
                "results_count": len(results) if results else 0
            })
        finally:
            logger.log_operation_time("notify_all_results", start_time)
        
        
        
        
