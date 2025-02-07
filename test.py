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
import time
import pyautogui
from pynput.keyboard import Key, Controller
pyautogui.getWindowsWithTitle("BloonsTD6")[0].activate()

pyautogui.moveTo(1400, 160, duration=0.5) # sniper monkey
keyboard = Controller()
keyboard.press('z')
time.sleep(0.1)
keyboard.release('z')

pyautogui.click()
keyboard.press('.')
time.sleep(0.1)
keyboard.release('.')
time.sleep(0.1)
keyboard.press('.')
time.sleep(0.1)
keyboard.release('.')
time.sleep(0.1)
# pyautogui.click()
# while True:
#     print(pyautogui.position())
#     time.sleep(2)
    
    