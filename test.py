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
from pynput import mouse
from locations import monkey_meadow

pyautogui.getWindowsWithTitle("BloonsTD6")[0].activate()
keyboard = Controller()
time.sleep(2)
for i in range(1,15):
    pyautogui.moveTo(monkey_meadow[i][0], monkey_meadow[i][1], duration=0.5)
    time.sleep(1)
    keyboard.press('q')
    time.sleep(0.1)
    keyboard.release('q')
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(1)
quit()
# pyautogui.moveTo(1400, 160, duration=0.5) # sniper monkey

# keyboard.press('z')
# time.sleep(0.1)
# keyboard.release('z')

# pyautogui.click()
# keyboard.press('.')
# time.sleep(0.1)
# keyboard.release('.')
# time.sleep(0.1)
# keyboard.press('.')
# time.sleep(0.1)
# keyboard.release('.')
# time.sleep(0.1)
# pyautogui.click()
# while True:
#     print(pyautogui.position())
#     time.sleep(2)

def on_click(x, y, button, pressed):
    if button == mouse.Button.left and pressed:
        print(f"Mouse clicked at ({x}, {y})")

# Set up the listener
with mouse.Listener(on_click=on_click) as listener:
    listener.join()