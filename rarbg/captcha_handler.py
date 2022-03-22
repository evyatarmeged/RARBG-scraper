import os
import pytesseract
import requests
from PIL import Image


# Get CAPTCHA image & extract text
class CaptchaHandler:

    def __init__(self):
        self.filename = 'solved_captcha.png'

    def get_captcha(self, img_data):
        with open(self.filename, 'wb') as captcha_image:
            captcha_image.write(img_data)
        return self.solve_captcha(self.filename)

    @staticmethod
    def solve_captcha(img_path):
        try:
            solution = pytesseract.image_to_string(Image.open(img_path))
            os.remove(img_path)  # Remove the file after solving
            return solution
        except FileNotFoundError:
            return
