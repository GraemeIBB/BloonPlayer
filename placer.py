import pyautogui
import time
from pynput.keyboard import Controller
from money_detector import MoneyDetector
from tower_costs import easy
from locations import monkey_meadow
from bindings import bindings



class Placer:
    def __init__(self):
        self.monkeys = []
        self.money = MoneyDetector()
        self.keyboard = Controller()
        # hardwired for easy on monkey meadow
        self.costs = easy
        self.map = monkey_meadow
        self.bind = bindings
        
    def placeNext(self, type):
       
        # Find the next available position
        if len(self.monkeys) > 0:
            available_positions = set(range(1, 15)) - {m[1] for m in self.monkeys}
            if not available_positions:
                print("No available positions")
                return
    
            next_position = min(available_positions)
            self.place(type, next_position)
        else:
            self.place(type,1)



    def place(self, type, location):
        # type example: "super_monkey"
        # location example: 1

        # check if monkey exists with that location already
        for m in self.monkeys:
            if m[1] == location:
                print("a monkey already exists in this location")
                return
        
        # check to see if you have enough money
        cost = self.costs.get(type + "000")
        if cost is None:
            print(f"Unknown tower type: {type}")
            return

        if int(self.money.get_money()) < cost:
            print("Not enough money to place this tower")
            return

        # place monkey
        key = bindings.get(type)
        self.goTo(location)
        self.keyboard.press(key)
        time.sleep(0.1)
        self.keyboard.release(key)
        time.sleep(0.1)
        pyautogui.click()


        # Add the new monkey to the list
        self.monkeys.append((type,location,"000"))
        print(f"Placed {type} at location {location}")
    
    def upgrade(self, monkey, choice):
        # monkey example: 1
        # choice example: "001"

        # check upgrade cost against current ballance
        # if viable then upgrade
        
        # determine which keybind through
        pass

    def goTo(self, location):
        coordinates = self.map.get(location)
        pyautogui.moveTo(coordinates, duration=0.5)
    
    def getMonkeysStr(self):
        return str(self.monkeys)

    

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