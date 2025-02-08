# Main goal is to play BTD6 solely using Python

import pyautogui
# import pytesseract
import time
from money_detector import MoneyDetector
from placer import Placer
from PIL import ImageGrab, ImageFilter, Image, ImageOps
import random
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

monDet = MoneyDetector()

pyautogui.getWindowsWithTitle("BloonsTD6")[0].activate()
place = Placer()
for i in range(1,4):
    place.placeNext("sniper_monkey")
    time.sleep(1)
print(place.getMonkeysStr())
# place.placeNext("wizard_monkey")
place.upgrade(0, 1)
place.upgrade(1, 2)
place.upgrade(2, 3)
place.upgrade(0, 1)
place.upgrade(0, 1)
place.upgrade(0, 2)
place.upgrade(0, 2)
print(place.getMonkeysStr())
print(str(place.thinkUpgrades()))
upgrades = place.thinkUpgrades()
if upgrades:
    chosen_upgrade = random.choice(upgrades)
    print(f"Chosen upgrade: {chosen_upgrade}")
    place.upgrade(chosen_upgrade[0], chosen_upgrade[1])
upgrades = place.thinkUpgrades()
if upgrades:
    chosen_upgrade = random.choice(upgrades)
    print(f"Chosen upgrade: {chosen_upgrade}")
    place.upgrade(chosen_upgrade[0], chosen_upgrade[1])
upgrades = place.thinkUpgrades()
if upgrades:
    chosen_upgrade = random.choice(upgrades)
    print(f"Chosen upgrade: {chosen_upgrade}")
    place.upgrade(chosen_upgrade[0], chosen_upgrade[1])

