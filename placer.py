import random
import pyautogui
import time
from pynput.keyboard import Key, Controller
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
        self.baseMonkeys = []
        for key in self.costs:
            if key[-3:] == "000":
                self.baseMonkeys.append(key)
        self.moveNum = 0
    
    def preciseMoney(self):
        a = self.money.get_money()
        b = self.money.get_money()
        if a == b:
            return a
        else:
            return self.preciseMoney()
        
    
    def placeNext(self, type):
       
        # Find the next available position
        if len(self.monkeys) > 0:
            available_positions = set(range(1, len(self.map))) - {m[1] for m in self.monkeys}
            if not available_positions:
                print("No available positions")
                return -1
    
            next_position = min(available_positions)
            self.place(type, next_position)
        else:
            self.place(type,1)
        return 1


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

        if int(self.preciseMoney()) < cost:
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
        self.monkeys.append([type,location,"000"])
        print(f"Placed {type} at location {location}")
    
    def upgrade(self, monkey, choice):
        if monkey < 0 or monkey >= len(self.monkeys):
            print("Invalid monkey index")
            return
        # monkey example: 0
        # choice example: 1 or 2 or 3
        newStr = ""
        m = self.monkeys[monkey]

        if choice == 1:
            keybind = self.bind['upgrade_path_1']
            newStr = str(int(m[2][choice-1]) + 1) +"00" 
        elif choice == 2:
            keybind = self.bind['upgrade_path_2']
            newStr = "0" + str(int(m[2][choice-1]) + 1)+"0" 
        elif choice == 3:
            keybind = self.bind['upgrade_path_3']
            newStr = "00" + str(int(m[2][choice-1]) + 1)
        else:
            print("Invalid upgrade choice")
            return 

        if m[0]+newStr not in self.costs:
            print(m[0]+newStr + " Invalid upgrade choice")
            return
        
        price = self.costs.get(m[0]+newStr)
        if(int(self.preciseMoney()) < price):
            print("Not enough money to upgrade this tower")
            return
        # upgrade monkey
        

        self.goTo(m[1])
        pyautogui.click()
        self.keyboard.press(keybind)
        time.sleep(0.1)
        self.keyboard.release(keybind)
        time.sleep(0.1)
        self.keyboard.press(Key.esc)
        time.sleep(0.1)
        self.keyboard.release(Key.esc)

        m[2] = m[2][:choice-1] + str(int(m[2][choice-1]) + 1) + m[2][choice:]
        print(f"Upgraded monkey at location {m[1]} with choice {choice}")
        

    def goTo(self, location):
        coordinates = self.map.get(location)
        pyautogui.moveTo(coordinates, duration=0.5)
    
    def getMonkeysStr(self):
        return str(self.monkeys)
    
    def getMoneyStr(self):
        return self.preciseMoney()
    
    def thinkUpgrades(self):
        # TODO make into a nested class think with methods like think.upgrade() and think.buy()

        # good idea is to evaluate all options with given money, then determine one that is most helpful.
        #  If all current monkeys are upgraded, then buy a new one.
        #  If none are, then upgrade them.
        # implement requirement logic here, ie if two paths have been upgraded, third is unavailable, and
        # if three upgrade have been made on one path, the limit for the other is 2.
        # --> placer.think()
        print('thinking-upgrade')
        viable = []
        i = 0
        for m in self.monkeys:
            # evaluating unavailable paths
            path1 = int(m[2][0])
            path2 = int(m[2][1])
            path3 = int(m[2][2])
            paths = [path1,path2,path3]
            selectedPaths = []
            j = 0
            for p in paths:
                if p > 0:
                    selectedPaths.append(j)
                j +=1

            path1Bool = True
            path2Bool = True
            path3Bool = True

            if(len(selectedPaths) == 2):
                print("two paths flagged")
                if(2 not in selectedPaths):
                    print("path 3 is unavailable")
                    path3Bool = False
                    if(path1 == 3):
                        print("path 2 is limited to 2")
                        if(path2 == 2):
                            path2Bool = False
                    elif(path2 == 3):
                        print("path 1 is limited to 2")
                        if(path1 == 2):
                            path1Bool = False
                    
                elif(1 not in selectedPaths):
                    print("path 2 is unavailable")
                    path2Bool = False
                    if(path1 == 3):
                        print("path 3 is limited to 2")
                        if(path3 == 2):
                            path3Bool = False
                    elif(path3 == 3):
                        print("path 1 is limited to 2")
                        if(path1 == 2):
                            path1Bool = False
                    
                elif(0 not in selectedPaths):
                    print("path 1 is unavailable")
                    path1Bool = False
                    if(path2 == 3):
                        print("path 3 is limited to 2")
                        if(path3 == 2):
                            path3Bool = False
                    elif(path3 == 3):
                        print("path 2 is limited to 2")
                        if(path2 == 2):
                            path2Bool = False
                    
            print(str(i)+" "+m[0]+ str(path1+1) +"00" + " option 1" + str(path1Bool))
            print(str(i)+" "+m[0]+ "0"+ str(path2+1) + "0" + " option 2" + str(path2Bool))
            print(str(i)+" "+m[0]+ "00"+ str(path3+1) + " option 3" + str(path3Bool))

            # checking costs against balance
            if path1Bool:
                if(m[0]+ str(path1+1) +"00" in self.costs ):
                    if(self.costs.get(m[0]+ str(path1+1) +"00") <= int(self.preciseMoney())):
                        viable.append([i,1,m])

            if path2Bool:
                if(m[0]+"0"+ str(path2+1) + "0" in self.costs):
                    if(self.costs.get(m[0]+"0"+ str(path2+1) + "0") <= int(self.preciseMoney())):
                        viable.append([i,2,m])

            if path3Bool:
                if(m[0]+"00"+ str(path3+1) in self.costs):
                    if(self.costs.get(m[0]+"00"+ str(path3+1)) <= int(self.preciseMoney())):
                        viable.append([i,3,m])
            i+=1
            

        return viable
    
    def thinkBuy(self):
        print('thinking-buy')
        # return list of possible buys in this format
        # [[type, location, value], [type, location, value],...] value is stored as a property due to how elements are appended out of order
        
        # iterate through list of monkeys in costs ending in 000, compare with balance
        viable = []
        for m in self.baseMonkeys:
            if(self.costs.get(m) <= int(self.preciseMoney())):
                viable.append([m ,0,0])
        # assign location
        for v in viable:
            pass
        return viable
        # assign value based on existing monkey types, the more of one kind there are, the less valuable
    
    def play(self):
        print("Move number: " + str(self.moveNum))
        thresh = 5
        if self.moveNum >= 30:
            thresh = 3
        if self.moveNum == 0:
            self.placeSniper()
            self.placeWizardNext()
            self.moveNum = 2
            return
        choice = random.randint(0,10)
        if choice > thresh:
            self.upgradeRandom()
        elif choice <= thresh:
            self.placeWizardNext()
        
        self.moveNum += 1
        
    
    def upgradeRandom(self):
        upgrades = self.thinkUpgrades()
        if upgrades:
            chosen_upgrade = random.choice(upgrades)
            print(f"Chosen upgrade: {chosen_upgrade}")
            self.upgrade(chosen_upgrade[0], chosen_upgrade[1])
        else:
            print("No upgrades available")
    
    def placeRandomNext(self):
        options = self.thinkBuy()
        if options:
            chosen_buy = random.choice(options)
            print(f"Chosen purchase: {chosen_buy}")
            self.placeNext(chosen_buy[0][:-3])
        else:
            print("No new monkeys available")
            
    def placeWizardNext(self):
        options = self.thinkBuy()
        for op in options:
            if op[0] == "wizard_monkey000":
                chosen_buy = op
                print(f"Chosen purchase: {chosen_buy}")
                self.placeNext(chosen_buy[0][:-3])
                return
    
    def placeSniper(self):
        self.place("sniper_monkey", 27)
        
        # FIXME: This is a temporary fix for the sniper monkey placement

    

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