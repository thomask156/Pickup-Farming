import sys
import win32api, win32gui, win32con
import time
import pyscreenshot as ImageGrab
from PyQt5.uic.properties import QtCore

from pynput.keyboard import Key, Controller
from pynput import keyboard as keybd

from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QApplication, QLabel, QCheckBox)
from PyQt5.QtWidgets import QTableView, QComboBox
from PyQt5 import *

class ReportExample(QWidget):

    def get_pixel_color(self):
        """Grabs a single pixel on the lower screen of the 3ds emulator,
         returning the color of this pixel in RGB format"""
        im = ImageGrab.grab(bbox=(750, 646, 751, 647))
        rgb_im = im.convert('RGB')
        r, g, b = rgb_im.getpixel((0, 0))
        return r, g, b

    def screen_change(self):
        """# Determines if a grabbed pixel is all black
        If it is black, then a battle has commenced"""
        color = self.get_pixel_color()[:]
        for pixel in color:
            if pixel is not 0:
                return False
        else:
            return True

    def on_press(self, key):
        """Listens for keypresses by the user, we check if the key is not the prev_key
        so that if it is the prev_key, the total time pressed will be recorded correctly"""
        if self.prev_key is not key:
            self.prev_key = key
            self.start = time.time()

    def convert(self, direction):
        """Converts keys into readable commands for the walking function, win32con and pynput use different codes
        takes a direction as an input, directions are one of the arrow keys being pressed"""
        up = win32con.VK_UP
        down = win32con.VK_DOWN
        left = win32con.VK_LEFT
        right = win32con.VK_RIGHT
        if direction == "down":
            return down, up
        if direction == "up":
            return up, down
        if direction == "left":
            return left, right
        if direction == "right":
            return right, left
        return "not a direction", "no u"

    def on_release(self, key):
        """The time from on_press is taken and is subtracted from current time to get them total time a key was pressed
        The direction pressed and for how long are added to the route
        If the user is recording their route to the pokemon center, then the mirrored route is also recorded"""
        finish = time.time()
        direction, opposite = self.convert(str(key)[4:])
        time_taken = finish - self.start
        if direction != "not a direction":
            if not self.poke_routeCheck:
                self.route.append((direction,  .8 * time_taken))
            else:
                self.poke_route.append((direction, .78 * time_taken))
                self.mirror_poke_route.insert(0, (opposite, .85 * time_taken))
        if key == keybd.Key.esc:
            # Stop listeners
            self.poke_routeCheck = False
            return False

    def __init__(self):
        """initializes the GUI as well as most elements including: the routes, direction conversions
        the listener and several boolean and variables used for recording user input"""
        super().__init__()
        self.initUI()
        self.state_left = win32api.GetKeyState(0x01)
        self.check_black = (1058, 670)  # this is a pixel on the lower screen we are going to check if it turns black
        self.up = win32con.VK_UP
        self.down = win32con.VK_DOWN
        self.left = win32con.VK_LEFT
        self.right = win32con.VK_RIGHT
        self.keyboard = Controller()
        self.PP = 30
        self.route = []
        self.poke_route = []
        self.mirror_poke_route = []
        self.poke_routeCheck = False
        self.prev_key = None
        self.listener = None
        self.hasPick = []
        self.hasHM = {}
        for i in range(1,7):
            self.hasHM[str(i)] = False

    def initPickCheckbox(self, name, x, y):
        """Initializes the pickup checkboxes
        Takes a name passed in from the initUI method as well as its x and y coordinates, placing it there"""
        self.b = QCheckBox(str(name), self)
        self.b.stateChanged.connect(self.clickBox)
        self.b.move(x, y)
        self.b.resize(320, 40)

    def initHMCheckbox(self, name, x, y):
        """Initializes the HM checkboxes to the right of the pickup checkboxes
        takes name of theckbox as well as its coordinates"""
        self.c = QCheckBox(str(name), self)
        self.c.stateChanged.connect(self.HMclickBox)
        self.c.move(x, y)
        self.c.resize(320, 40)

    def clickBox(self, state):
        """Records which slots have pokemon with pickup
        State: whether the button has been checked or unchecked"""
        source = self.sender()
        if state == QtCore.Qt.Checked:
            for i in range(1, 7):
                if source.text() == str(i):
                    self.hasPick.append(i)
        else:
            for i in range(1,7):
                if source.text() == str(i):
                    self.hasPick.remove(i)

    def HMclickBox(self, state):
        """Records which slots have pokemon with HM moves
        State: whether the button has been checked or unchecked"""
        source = self.sender()
        if state == QtCore.Qt.Checked:
            for i in range(1, 7):
                if source.text()[5] == str(i):
                    self.hasHM[str(i)] = True
        else:
            for i in range(1, 7):
                if source.text()[5] == str(i):
                    self.hasHM[str(i)] = False

    def battled(self):
        """Used to subtract from the PP count"""
        self.PP = self.PP - 1

    def keypress(self, key):
        """Used for keypresses in methods like check_poke and pickup
        It takes a key as input and presses it for a certain amount of time"""
        time.sleep(.2)
        self.keyboard.press(key)
        time.sleep(.1)
        self.keyboard.release(key)
        time.sleep(.2)

    def check_poke(self, hasHM):
        """Takes item held by the pokemon in the current slot
        hasHM: boolean determining if the pokemon has an HM move"""
        self.keypress('a')
        self.keypress(Key.down)
        self.keypress(Key.down)
        if hasHM:
            self.keypress(Key.down)
        self.keypress('a')
        self.keypress(Key.down)
        self.keyboard.press('a')
        time.sleep(.2)
        self.keyboard.release('a')
        time.sleep(.2)
        self.keyboard.press('a')
        time.sleep(.2)
        self.keyboard.release('a')

    def move_to(self, fron, to):
        """This moves between slots occupied by pokemon with pickup,
        fron: the slot which has just been checked
        to: the slot which needs to be checked next"""
        if fron is to:
            return
        elif fron % 2 == to % 2:
            steps = int((to-fron)/2)
            for i in range(steps):
                time.sleep(.1)
                self.keypress(Key.down)
        else:
            self.keypress(Key.right)
            steps = int((to - (fron+1)) / 2)
            for i in range(steps):
                time.sleep(.1)
                self.keypress(Key.down)

    def pickup(self):
        """Goes to each slot occupied by a pickup pokemon, running check_poke() on each slot
        ultimately collects items from each of the slots with a pickup pokemon"""
        time.sleep(1)
        self.keypress('z')
        self.keyboard.press('a')
        time.sleep(.3)
        self.keyboard.release('a')
        time.sleep(1)
        size = self.hasPick.__len__()
        if size is not 0:
            self.hasPick.sort()
            self.move_to(1, self.hasPick[0])
            for i in range(0, size):
                self.check_poke(self.hasHM[str(self.hasPick[i])])
                if i < size - 1:
                    self.move_to(self.hasPick[i], self.hasPick[i + 1])
        self.keypress('z')
        time.sleep(4)

    def battle_attack(self):
        """Runs the battle protocol, which is to use the first ability and
        one-hit KO the wild pokemon"""
        time.sleep(7)
        self.keyboard.press('a')
        time.sleep(.3)
        self.keyboard.release('a')
        time.sleep(.5)
        self.keyboard.press('a')
        time.sleep(.3)
        self.keyboard.release('a')
        self.battled()
        time.sleep(7)
        time.sleep(.3)
        self.pickup()

    def battle_flee(self):
        """Flee protocol, the user runs from the wild pokemon, not fighting whenever this is called"""
        time.sleep(6)
        self.keypress(Key.down)
        time.sleep(.2)
        self.keypress(Key.right)
        self.keyboard.press('a')
        time.sleep(.1)
        self.keyboard.release('a')
        time.sleep(5)

    def walk(self, direction, dur,
             battle):
        """Method used to walk the route as well as return to the pokemon center if necessary
        direction: the direction in which the bot walks
        dur: the duration for which the bot walks in that direction
        battle:boolean variable determining if the bot fights or runs from battle"""
        win32api.keybd_event(direction, 0, 0, 0)
        start = time.time()
        stop = time.time() + dur
        while time.time() < stop:
            time.sleep(.01)
            if self.screen_change():
                time.sleep(.3)
                win32api.keybd_event(direction, 0, win32con.KEYEVENTF_KEYUP, 0)
                time.sleep(.2)
                if battle:
                    self.battle_attack()
                else:
                    self.battle_flee()
                    self.walk(direction, stop-start, False)
            win32api.keybd_event(direction, 0, 0, 0)
        win32api.keybd_event(direction, 0, win32con.KEYEVENTF_KEYUP, 0)

    def initUI(self):
        """Creates the buttons and checkboxes needed for the GUI"""
        self.createBtn("Run Pickup", 10, 10)
        self.createBtn('Record Route', 10, 60)
        self.createBtn('Run Route', 10, 110)
        self.createBtn('Show Route', 10, 160)
        self.createBtn('Clear Route', 10, 210)
        self.createBtn('Poke Center', 10, 260)
        self.createBtn('Poke Route', 10, 310)
        self.createBtn('Clear Poke Route', 150, 310)
        for i in range(1,7):
            self.initPickCheckbox(i, 150, 25*i)
        for i in range(1,7):
            self.initHMCheckbox("slot "+str(i)+" has HM", 200, 25*i)
        self.pickupLabel = QLabel("Select Which Pokemon Have Pickup As Well As If They Have HM Moves", self)
        self.pickupLabel.move(150, 10)
        self.setGeometry(300, 300, 650, 400)
        self.setWindowTitle('Poke Bot')
        self.show()

    def createBtn(self, name, x, y):
        """Creates button on GUI, takes the name of the button and its x-y coordinates
        """
        self.pokeBtn = QPushButton(name, self)
        self.pokeBtn.setCheckable(True)
        self.pokeBtn.move(x, y)
        self.pokeBtn.clicked[bool].connect(self.handleBtn)


    def run_route(self):
        """Iterates through the route indefinitely, when self.PP becomes 1
         the bot returns to the pokemon center, healing then returning to the route"""
        time.sleep(2)
        while self.PP > 0:
            for r in self.route:
                if self.PP is 1:
                    self.pokeCenter()
                time.sleep(.1)
                self.walk(r[0], r[1], 1)

    def pokeCenter(self):
        """ Routing to the pokemon center, iterates through poke route,
        runs the healing transaction and then returns to origin point"""
        # self.walk(self.up, 3, 0)
        # time.sleep(.2)
        # self.walk(self.right, 4, 0)
        # time.sleep(.2)
        # self.walk(self.up, 3, 0)
        # time.sleep(.2)
        # self.walk(self.left, 3, 0)
        # time.sleep(.2)
        # self.walk(self.up, 2, 0)
        # time.sleep(.2)
        # self.walk(self.left, .4, 0)
        # time.sleep(.2)
        # self.walk(self.up, 1, 0)
        # time.sleep(.2)
        # self.walk(self.left, .68, 0)
        # time.sleep(.2)
        # self.walk(self.up, 4, 0)
        for step in self.poke_route:
            self.walk(step[0], step[1], 0)
        self.keypress('a')
        time.sleep(1)
        self.keypress('a')
        time.sleep(1)
        self.keypress('a')
        time.sleep(5)
        self.keypress('a')
        time.sleep(.5)
        self.keypress('a')
        time.sleep(.5)
        self.keypress('a')  # your pokemon have been fully healed!
        time.sleep(.1)
        # self.walk(self.down, 2, 0)
        # time.sleep(.1)
        # self.walk(self.right, .6, 0)
        # time.sleep(.1)
        # self.walk(self.down, 4, 0)
        # self.walk(self.left, .7, 0)
        for step in self.mirror_poke_route:
            time.sleep(.2)
            self.walk(step[0], step[1], 0) # should return us to our original position
        self.PP = 30

    def handleBtn(self):
        """Handles button inputs for PyQt5"""
        source = self.sender()
        self.hasPick.sort()
        if source.text() == "Run Pickup":
            # TODO: make the calls to run the appropriate query and get the model
            print("starting to pick up")
            self.pickup()
        if source.text() == "Run Route":
            # TODO: make the calls to run the appropriate query and get the model
            self.run_route()
        if source.text() == "Record Route":
            with keybd.Listener(
                    on_press=self.on_press,
                    on_release=self.on_release) as self.listener:
                self.listener.join()
        if source.text() == "Show Route":
            print(self.route)
        if source.text() == "Clear Route":
            self.route = []
        if source.text() == "Poke Center":
            time.sleep(2)
            self.pokeCenter()
        if source.text() == "Poke Route":
            self.poke_routeCheck = True
            with keybd.Listener(
                    on_press=self.on_press,
                    on_release=self.on_release) as self.listener:
                self.listener.join()
        elif source.text() == "Clear Poke Route":
            self.poke_route = []
            self.mirror_poke_route = []

    def onActivated(self, text):
        self.genreLbl.setText(text)
        self.genreLbl.adjustSize()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ReportExample()
    sys.exit(app.exec_())