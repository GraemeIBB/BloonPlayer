# Main goal is to play BTD6 solely using Python

import pyautogui
# import pytesseract
import time
from money_detector import MoneyDetector
from placer import Placer
from PIL import ImageGrab, ImageFilter, Image, ImageOps
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

monDet = MoneyDetector()

pyautogui.getWindowsWithTitle("BloonsTD6")[0].activate()
place = Placer()
# for i in range(1,5):
#     place.placeNext("wizard_monkey")
#     time.sleep(2)
# print(place.getMonkeysStr())
place.placeNext("wizard_monkey")
place.upgrade(0, 1)
print(place.getMonkeysStr())

