import cv2
import numpy as np
from transformers import pipeline
import os
from utils.config import get_env_var
from utils.logger import logger

# Initialize the OCR pipeline for image-to-text conversion
pipe = pipeline("image-to-text", model="microsoft/trocr-large-printed")

class CaptchaSolver:
    def __init__(self, image_path):
        """
        Initialize the CaptchaSolver with the given image path.
        
        Args:
            image_path (str): Path to the captcha image
        """
        self.image = cv2.imread(image_path)
        self.kernel = np.ones((2, 2), np.uint8)
        # Get data folder path from environment variables
        self.data_folder = get_env_var("SCREENSHOTS_FOLDER")
        # Ensure data folder exists
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)

    def enhance_legibility(self, cropped_image):
        """
        Convert the image to grayscale to enhance text legibility.
        
        Args:
            cropped_image: The image to enhance
            
        Returns:
            Grayscale version of the input image
        """
        gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        return gray

    def clean_number(self, text):
        """
        Remove any non-digit characters from the text.
        
        Args:
            text (str): Text to clean
            
        Returns:
            str: Cleaned text containing only digits
        """
        return ''.join(filter(str.isdigit, text))

    def math_operation(self, left_number, right_number):
        """
        Perform addition operation on the cleaned numbers.
        
        Args:
            left_number: First number
            right_number: Second number
            
        Returns:
            int: Result of the addition operation
        """
        try:
            # Clean both numbers before processing
            left_number = self.clean_number(str(left_number))
            right_number = self.clean_number(str(right_number))
            
            if right_number.isdigit():
                result = eval(f"{left_number} + {right_number}")
                logger.debug(f"Operation: {left_number} + {right_number} = {result}")
                return result
            logger.warning(f"Right number not a digit after cleaning: {right_number}")
            return None
        except Exception as e:
            logger.error(f"Error in math_operation: {e}")
            return None

    def resolve(self, left_image, right_image, left_image_twice, right_image_twice):
        """
        Resolve the captcha by attempting to read numbers from different image versions.
        
        Args:
            left_image: Path to the left unit number image
            right_image: Path to the right unit number image
            left_image_twice: Path to the left twice number image
            right_image_twice: Path to the right twice number image
            
        Returns:
            int: Result of the captcha calculation or None if failed
        """
        logger.info("Attempting to resolve captcha...")
        
        # First attempt with twice images
        left_number = pipe(left_image_twice)[0]['generated_text']
        logger.debug(f"Left number (twice): {left_number}")
        
        if left_number.isdigit():
            left_number = int(left_number)
            if left_number < 10 or left_number == None or left_number == "":
                logger.debug("Left number < 10, trying unit image")
                left_number = pipe(left_image)[0]['generated_text']
                right_number = pipe(right_image_twice)[0]['generated_text']
                logger.debug(f"New left number: {left_number}, Right number: {right_number}")
                
                if right_number.isdigit() and int(right_number) > 10:
                    return self.math_operation(left_number, right_number)
                else:
                    right_number = pipe(right_image)[0]['generated_text']
                    logger.debug(f"Using unit right number: {right_number}")
                    return self.math_operation(left_number, right_number)
            elif left_number >= 10:
                right_number = pipe(right_image_twice)[0]['generated_text']
                logger.debug(f"Using twice right number: {right_number}")
                return self.math_operation(left_number, right_number)
        else:
            logger.debug("Left number not a digit, trying unit image")
            left_number = pipe(left_image)[0]['generated_text']
            if left_number.isdigit():
                right_number = pipe(right_image)[0]['generated_text']
                logger.debug(f"New left number: {left_number}, Right number: {right_number}")
                return self.math_operation(left_number, right_number)
        
        logger.error("Failed to resolve captcha")
        return None

    def solve_captcha(self):
        """
        Main method to solve the captcha by processing different parts of the image.
        
        Returns:
            int: Result of the captcha calculation or None if failed
        """
        # Define positions and dimensions for image cropping
        positions = {'left': 10, 'right_unit': 80, 'right_twice': 90}
        dimensions = {'width_twice': 40, 'width_unit': 25, 'height': 25}
        
        # Crop different parts of the image for number recognition
        left_image_for_unit_number = self.image[7:30, positions['left']:positions['left']+dimensions['width_unit']]
        left_image_for_twice_number = self.image[7:30, positions['left']:positions['left']+dimensions['width_twice']]
        right_image_for_left_twice_number = self.image[7:30, positions['right_twice']:positions['right_twice']+dimensions['width_twice']]
        right_image_for_left_unit_number = self.image[7:30, positions['right_unit']:positions['right_unit']+dimensions['width_twice']]

        # Enhance legibility of all cropped images
        left_enhanced = self.enhance_legibility(left_image_for_unit_number)
        left_enhanced_for_twice_number = self.enhance_legibility(left_image_for_twice_number)
        right_enhanced = self.enhance_legibility(right_image_for_left_unit_number)
        right_enhanced_for_twice_number = self.enhance_legibility(right_image_for_left_twice_number)

        # Save enhanced images to data folder
        left_image_path = os.path.join(self.data_folder, 'left_number.png')
        left_twice_path = os.path.join(self.data_folder, 'left_image_for_twice_number.png')
        right_image_path = os.path.join(self.data_folder, 'right_number.png')
        right_twice_path = os.path.join(self.data_folder, 'right_image_for_twice_number.png')

        cv2.imwrite(left_image_path, left_enhanced)
        cv2.imwrite(left_twice_path, left_enhanced_for_twice_number)
        cv2.imwrite(right_image_path, right_enhanced)
        cv2.imwrite(right_twice_path, right_enhanced_for_twice_number)

        return self.resolve(left_image_path, right_image_path, left_twice_path, right_twice_path)
