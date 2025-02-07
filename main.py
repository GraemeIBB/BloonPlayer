# Main goal is to play BTD6 solely using Python

import pyautogui
import pytesseract
import time
from money_detector import MoneyDetector
from PIL import ImageGrab, ImageFilter, Image, ImageOps
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

det = MoneyDetector()

while True:
    # money = det.get_money()
    # print(money)
    time.sleep(2)

# pyautogui.moveTo(450, 75, duration=0.5)


 # wizard monkey -> A
    # Super monkey -> S
    # Bomb shooter -> E
    # Sniper monkey -> Z
    # Banana farm -> H
    
    # Upgrade path 1 -> ,
    # Upgrade path 2 -> .
    # Upgrade path 3 -> /
    
    # Change target -> Tab
    
    # Sell -> backspace
    