import requests
from utils.logger import logger
from utils.config import get_env_var

# Get the ntfy.sh topic from environment variables
topic = get_env_var("TOPIC")

def send_notification(message: str):
    """
    Send a notification using ntfy.sh service.
    
    Args:
        message (str): The message content to be sent in the notification
        
    Raises:
        requests.exceptions.RequestException: If the notification fails to send
    """
    try:
        # Log the attempt to send notification
        logger.info(f"Sending notification with message: {message}")
        
        # Send POST request to ntfy.sh with the message and headers
        response = requests.post(f"https://ntfy.sh/{topic}",
                     data=message.encode("utf-8"),
                     headers={
                         "Title": "Beykent Sınav Sonucunuz Açıklandı !",
                         "Tags": "loudspeaker"
                         })
        
        # Check if the request was successful (raises exception for 4xx/5xx status codes)
        response.raise_for_status()
        
        # Log successful notification
        logger.info("Notification sent successfully")
        
    except requests.exceptions.RequestException as e:
        # Log the error and re-raise the exception for handling in the calling code
        logger.error(f"Failed to send notification: {str(e)}")
        raise

