import requests
from utils.logger import logger
from utils.config import get_env_var
from pages.results_page import Result

class Notification:
    def __init__(self):
        logger.info("Initializing Notification")
        self.topic = get_env_var("TOPIC")

    def send_alert(self, message: str):
        url = f"https://ntfy.sh/{self.topic}"
        headers = {
            "Title": "beykent universitesi iletisim bilgilerinizi guncelleyiniz",
            "Tags": "warning",
            "Priority": "high"
        }
        try:
            response = requests.post(
                url,
                data=message.encode("utf-8"),
                headers=headers
            )
            response.raise_for_status()
            logger.info(f"Alert sent successfully: {message}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send alert: {str(e)}")

    def send_notification(self, result: Result):
        message = f"Sınav sonucunuz açıklandı!\n\nDers: {result.lesson_name}\nSınav: {result.exam_type}\nNot: {result.score}"

        url = f"https://ntfy.sh/{self.topic}"

        headers = {
            "Title": "Beykent Universitesi Sinav Sonucunuz Aciklandi !",
            "Tags": "loudspeaker",
            "Priority": "high"
        }

        try:
            response = requests.post(
                url,
                data=message.encode("utf-8"),
                headers=headers
            )
            response.raise_for_status()
            logger.info(f"Notification sent successfully for {result.lesson_name} {result.exam_type} with score {result.score}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send notification: {str(e)}")
    
    def notify_new_results(self, results: list[Result]):
        if not results:
            logger.info("No new results to notify")
            return
        for result in results:
            self.send_notification(result)
        
        
        
        
