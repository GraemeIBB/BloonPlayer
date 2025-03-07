import pyautogui
import time
from placer import Placer
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

pyautogui.getWindowsWithTitle("BloonsTD6")[0].activate()
place = Placer()
place.placeWizardNext()
place.placeWizardNext()
place.placeWizardNext()
place.placeWizardNext()
place.placeWizardNext()
while True:
    place.upgradeRandom()
    print(place.getMonkeysStr())
