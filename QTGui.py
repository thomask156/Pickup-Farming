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

    # this grabs a single pixel on the lower screen of the 3ds emulator, and returns the color of this pixel
    def get_pixel_color(self):
        im = ImageGrab.grab(bbox=(750, 646, 751, 647))
        rgb_im = im.convert('RGB')
        r, g, b = rgb_im.getpixel((0, 0))
        return r, g, b

    # this determines if the grabbed pixel is all black, AKA a battle has started
    def screen_change(self):
        color = self.get_pixel_color()[:]
        for pixel in color:
            if pixel is not 0:
                return False
        else:
            return True

    # this is a listener function, listening for when a key is pressed and recording when it it pressed
    def on_press(self, key):
        print(key)
        if self.prev_key is not key:
            self.prev_key = key
            self.start = time.time()

    # this method converts keys into readable commands for the walking function, win32con and pynput use different codes

    def convert(self, direction):
        up = win32con.VK_UP         # directions used by win32con for input into the 3ds emulator
        down = win32con.VK_DOWN     # I also give the opposite direction in case the route can be mirrored
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
        return "not a direction", "no u"  # here we only want to record arrow key inputs

    # for this method, we take the time from earlier and subtract that from the current time to get the delay
    # we add on the direction pressed and the delay to our route
    def on_release(self, key):
        finish = time.time()
        direction, opposite = self.convert(str(key)[4:])
        if direction != "not a direction":
            time_taken = finish - self.start
            self.route.append((direction,  .8 * time_taken))
        if key == keybd.Key.esc:
            # Stop listener
            return False

    # lotta bad boys here, prev key is used to see if the same key is being held down, and to make sure the delays work correctly
    def __init__(self):
        super().__init__()
        self.initUI()
        self.state_left = win32api.GetKeyState(0x01)
        self.check_black = (1058, 670)  # this is a pixel on the lower screen we are going to check if it turns black
        self.up = win32con.VK_UP
        self.down = win32con.VK_DOWN
        self.left = win32con.VK_LEFT
        self.right = win32con.VK_RIGHT
        self.keyboard = Controller()
        self.PP = 25
        self.route = []
        self.prev_key = None
        self.listener = None
        self.hasPick = []
        self.hasHM = {}
        for i in range(1,7):
            self.hasHM[str(i)] = False

    # initializer for the left checkbox
    def initPickCheckbox(self, name, x, y):
        self.b = QCheckBox(str(name), self)
        self.b.stateChanged.connect(self.clickBox)
        self.b.move(x, y)
        self.b.resize(320, 40)

    # initializer for the HM checkboxes
    def initHMCheckbox(self, name, x, y):
        self.c = QCheckBox(str(name), self)
        self.c.stateChanged.connect(self.HMclickBox)
        self.c.move(x, y)
        self.c.resize(320, 40)

    # this says which slots are occupied by pickup pokemon, and therefore which slots we have to go to
    def clickBox(self, state):
        source = self.sender()
        if state == QtCore.Qt.Checked:
            for i in range(1, 7):
                if source.text() == str(i):
                    self.hasPick.append(i)
        else:
            for i in range(1,7):
                if source.text() == str(i):
                    self.hasPick.remove(i)

    # much like above, this function serves to say if we need to do an extra step because this pokemon has an HM
    # this uses a dictionary to store the boolean about if the pokemon has an HM move
    def HMclickBox(self, state):
        source = self.sender()
        if state == QtCore.Qt.Checked:
            for i in range(1, 7):
                if source.text()[5] == str(i):
                    self.hasHM[str(i)] = True
        else:
            for i in range(1, 7):
                if source.text()[5] == str(i):
                    self.hasHM[str(i)] = False

    # small method which is the only place to edit PP
    def battled(self):
        self.PP = self.PP - 1

    # main method used to input key presses, the reason we don't use win32con here is because pynput can't do key holds
    # only presses
    def keypress(self, key):
        time.sleep(.2)
        self.keyboard.press(key)
        time.sleep(.1)
        self.keyboard.release(key)
        time.sleep(.2)

    # this is just the automation of taking the picked up item from the pokemon
    def check_poke(self, hasHM):
        self.keypress('a')
        self.keypress(Key.down)
        self.keypress(Key.down)
        if hasHM:
            self.keypress(Key.down)
        self.keypress('a')
        self.keypress(Key.down)
        self.keyboard.press('a')
        time.sleep(.3)
        self.keyboard.release('a')
        time.sleep(.3)
        self.keyboard.press('a')
        time.sleep(.3)
        self.keyboard.release('a')

    # This moves between slots occupied by pokemon with pickup, I wanted it to be to and from but from is a keyword
    def move_to(self, fron, to):
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

    # this automates the process of going between the pokemon, and running check_poke on each one
    # it gets a bit clunky when checking wether the poke has an HM or not, as I didn't want to use tuples to store position and HM
    def pickup(self):
        print("pickup")
        time.sleep(1)
        self.keypress('z')
        self.keyboard.press('a')
        time.sleep(.3)
        self.keyboard.release('a')
        time.sleep(.7)
        time.sleep(1.5)
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

    # very basic battle script, uses the first move from the first pokemon, expecting a one shot KO
    def battle_attack(self):
        print("battle")
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

    #this function is called when we don't have enough PP to fight and just want to go to the poke center
    def battle_flee(self):
        time.sleep(6)
        self.keypress(Key.down)
        time.sleep(.2)
        self.keypress(Key.right)
        self.keyboard.press('a')
        time.sleep(.1)
        self.keyboard.release('a')
        time.sleep(5)

    def walk(self, direction, dur,
             battle):  # here we set the direction we want to walk in, the time we walk here, and if we battle or not
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

    # buttons and checklist are initialized here
    def initUI(self):
        self.createBtn("Run Pickup", 10, 10)
        self.createBtn('Record Route', 10, 60)
        self.createBtn('Run Route', 10, 110)
        self.createBtn('Show Route', 10, 160)
        self.createBtn('Clear Route', 10, 210)
        self.createBtn('Poke Center', 10, 260)
        for i in range(1,7):
            self.initPickCheckbox(i, 150, 25*i)
        for i in range(1,7):
            self.initHMCheckbox("slot "+str(i)+" has HM", 200, 25*i)
        self.pickupLabel = QLabel("Select Which Pokemon Have Pickup As Well As If They Have HM Moves", self)
        self.pickupLabel.move(150, 10)
        self.setGeometry(300, 300, 650, 400)
        self.setWindowTitle('Poke Bot')
        self.show()

    # simple method to create each button, coordinates and name of button passed
    def createBtn(self, name, x, y):
        self.pokeBtn = QPushButton(name, self)
        self.pokeBtn.setCheckable(True)
        self.pokeBtn.move(x, y)
        self.pokeBtn.clicked[bool].connect(self.handleBtn)

    # this iterates through the route indefinitely, healing when the PP gets too low
    def run_route(self):
        time.sleep(2)
        while self.PP > 0:
            for r in self.route:
                if self.PP is 1:
                    self.pokeCenter()
                time.sleep(.1)
                self.walk(r[0], r[1], 1)

    # manual insertion of the route to the pokecenter, unfortunately with how pyqt interacts with the emulator, the
    # times aren't always accurate, which can lead to frustration
    def pokeCenter(self):
        self.walk(self.up, 3, 0)
        time.sleep(.2)
        self.walk(self.right, 4, 0)
        time.sleep(.2)
        self.walk(self.up, 3, 0)
        time.sleep(.2)
        self.walk(self.left, 3, 0)
        time.sleep(.2)
        self.walk(self.up, 2, 0)
        time.sleep(.2)
        self.walk(self.left, .4, 0)
        time.sleep(.2)
        self.walk(self.up, 1, 0)
        time.sleep(.2)
        self.walk(self.left, .68, 0)
        time.sleep(.2)
        self.walk(self.up, 4, 0)
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
        self.keypress('a')
        time.sleep(.1)
        self.walk(self.down, 2, 0)
        time.sleep(.1)
        self.walk(self.right, .6, 0)
        time.sleep(.1)
        self.walk(self.down, 4, 0)
        self.walk(self.left, .65, 0)
        self.PP = 5

    # method used to handle button inputs, listener is started in here, every button is self-explanatory
    def handleBtn(self):
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
        elif source.text() == "Poke Center":
            self.pokeCenter()

    # useless at the moment
    def onActivated(self, text):
        self.genreLbl.setText(text)
        self.genreLbl.adjustSize()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ReportExample()
    sys.exit(app.exec_())