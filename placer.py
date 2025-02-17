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
                # print("No available positions")
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
                # print("a monkey already exists in this location")
                return
        
        # check to see if you have enough money
        cost = self.costs.get(type + "000")
        if cost is None:
            # print(f"Unknown tower type: {type}")
            return

        if int(self.preciseMoney()) < cost:
            # print("Not enough money to place this tower")
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
        # print(f"Placed {type} at location {location}")
    
    def upgrade(self, monkey, choice):
        if monkey < 0 or monkey >= len(self.monkeys):
            # print("Invalid monkey index")
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
            # print("Invalid upgrade choice")
            return 

        if m[0]+newStr not in self.costs:
            # print(m[0]+newStr + " Invalid upgrade choice")
            return
        
        price = self.costs.get(m[0]+newStr)
        if(int(self.preciseMoney()) < price):
            # print("Not enough money to upgrade this tower")
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
        # print(f"Upgraded monkey at location {m[1]} with choice {choice}")
        

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
        # print('thinking-upgrade')
        viable = []
        i = 0
        for m in self.monkeys:
            # evaluating unavailable paths
            path1 = int(m[2][0])
            path2 = int(m[2][1])
            path3 = int(m[2][2])

            # Build a small dictionary to hold path values & booleans by index
            paths_dict = {
                0: {"value": path1, "flag": True},
                1: {"value": path2, "flag": True},
                2: {"value": path3, "flag": True},
            }

            # Which path indexes are actually "selected" (i.e., > 0)?
            selectedPaths = [i for i, p in enumerate([path1, path2, path3]) if p > 0]

            # If exactly two paths are selected, disable the missing path’s flag
            # and then see if one path being >=3 should disable another which is ==2.
            if len(selectedPaths) == 2:
                # 1) Identify the path that is *not* selected
                missing = ({0, 1, 2} - set(selectedPaths)).pop()
                paths_dict[missing]["flag"] = False

                # 2) Among the remaining two:
                remaining = list(set([0, 1, 2]) - {missing})
                i, j = remaining[0], remaining[1]

                # 3) If one is >= 3 and the other is exactly 2, disable the "2" path
                if paths_dict[i]["value"] >= 3 and paths_dict[j]["value"] == 2:
                    paths_dict[j]["flag"] = False
                elif paths_dict[j]["value"] >= 3 and paths_dict[i]["value"] == 2:
                    paths_dict[i]["flag"] = False

            

                    
            # print(str(i)+" "+m[0]+ str(path1+1) +"00" + " option 1" + str(path1Bool))
            # print(str(i)+" "+m[0]+ "0"+ str(path2+1) + "0" + " option 2" + str(path2Bool))
            # print(str(i)+" "+m[0]+ "00"+ str(path3+1) + " option 3" + str(path3Bool))

            # checking costs against balance
            if paths_dict[0]["flag"]:
                if(m[0]+ str(path1+1) +"00" in self.costs ):
                    if(self.costs.get(m[0]+ str(path1+1) +"00") <= int(self.preciseMoney())):
                        viable.append([i,1,m])

            if paths_dict[1]["flag"]:
                if(m[0]+"0"+ str(path2+1) + "0" in self.costs):
                    if(self.costs.get(m[0]+"0"+ str(path2+1) + "0") <= int(self.preciseMoney())):
                        viable.append([i,2,m])

            if paths_dict[2]["flag"]:
                if(m[0]+"00"+ str(path3+1) in self.costs):
                    if(self.costs.get(m[0]+"00"+ str(path3+1)) <= int(self.preciseMoney())):
                        viable.append([i,3,m])
            i+=1
            

        return viable
    
    def thinkBuy(self):
        # print('thinking-buy')
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
        # print("Move number: " + str(self.moveNum))
        thresh = 5
        if self.moveNum >= 30:
            thresh = 3
        if self.moveNum == 0:
            self.placeSniper()
            self.placeWizardNext()
            self.moveNum = 2
            return
        choice = random.randint(0,10)
        if(len(self.monkeys) > 14):
            self.upgradeRandom()
            self.moveNum += 1
            return
        if choice > thresh:
            self.upgradeRandom()
        elif choice <= thresh:
            self.placeWizardNext()
        
        
        
    
    def upgradeRandom(self):
        upgrades = self.thinkUpgrades()
        if upgrades:
            chosen_upgrade = random.choice(upgrades)
            # print(f"Chosen upgrade: {chosen_upgrade}")
            self.upgrade(chosen_upgrade[0], chosen_upgrade[1])
        
    
    def placeRandomNext(self):
        options = self.thinkBuy()
        if options:
            chosen_buy = random.choice(options)
            # print(f"Chosen purchase: {chosen_buy}")
            self.placeNext(chosen_buy[0][:-3])
        else:
            pass
            # print("No new monkeys available")
            
    def placeWizardNext(self):
        options = self.thinkBuy()
        for op in options:
            if op[0] == "wizard_monkey000":
                chosen_buy = op
                # print(f"Chosen purchase: {chosen_buy}")
                # find an available location
                # choose a random (or strategic) location

                self.placeNext(chosen_buy[0][:-3])
                return
    
    def placeSniper(self):
        self.place("sniper_monkey", 27)
        
        # FIXME: This is a temporary fix for the sniper monkey placement