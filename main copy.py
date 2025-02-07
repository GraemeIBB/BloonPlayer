# Main goal is to play BTD6 solely using Python

import pyautogui
import pytesseract
import time
from PIL import ImageGrab, ImageFilter, Image, ImageOps
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

# money region
x,y,x2,y2= 365,0,570,100
region = (x,y,x2,y2)

def process_image(img):
    """Prepares image for OCR by applying filters."""
    img = img.convert("L")  # Convert to grayscale
    img = ImageOps.invert(img)  # Invert colors if needed
    img = img.filter(ImageFilter.SHARPEN)  # Sharpen for better OCR
    img = img.point(lambda p: p > 180 and 255)  # Binarization (adjust threshold)
    return img
while True:
    Money = ImageGrab.grab(region)
    Money = Money.resize((Money.width * 3, Money.height * 3), Image.LANCZOS)
    
    Money = process_image(Money)
    Money.show()
    text = pytesseract.image_to_string(Money, config="--psm 6 -c tessedit_char_whitelist=0123456789")

    print(text)
    if text.strip() == "":
        # continue
        pass
    time.sleep(2)
    break

# pyautogui.moveTo(450, 75, duration=0.5)