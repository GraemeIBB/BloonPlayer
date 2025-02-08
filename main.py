# Main goal is to play BTD6 solely using Python

import pyautogui
import time
from placer import Placer
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

pyautogui.getWindowsWithTitle("BloonsTD6")[0].activate()
place = Placer()
while True:
    place.play()
    print(place.getMoneyStr())
    print(place.getMonkeysStr())
    time.sleep(3)

