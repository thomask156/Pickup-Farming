import sys
import win32api, win32gui, win32con
import time
import pyscreenshot as ImageGrab

from pynput.keyboard import Key, Controller
from pynput import keyboard as keybd
from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QApplication, QLabel)
from PyQt5.QtWidgets import QTableView, QComboBox

##Things to add:
## -Select Which Slots have pickup bots
## -Select which mons have HM moves
## -Let people know that the bot can be inconsistent because windows sucks


class ReportExample(QWidget):

    def get_pixel_color(self):
        im = ImageGrab.grab(bbox=(750, 646, 751, 647))
        rgb_im = im.convert('RGB')
        r, g, b = rgb_im.getpixel((0, 0))
        return r, g, b

    # need to use somehting other than get pixel color as it is currently
    # thinking of using pyscreenshot on a small area of the screen (1x1 lol) and then checking that value

    def screen_change(self):
        color = self.get_pixel_color()[:]
        for pixel in color:
            if pixel is not 0:
                return False
        else:
            return True

    def on_press(self, key):
        print(key)
        if self.prev_key is not key:
            self.prev_key = key
            self.start = time.time()

    def convert(self, direction):
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
        return "you're mom gay", "no u"

    def on_release(self, key):
        self.prev_key
        self.start
        self.route
        finish = time.time()
        direction, opposite= self.convert(str(key)[4:])
        if direction != "you're mom gay":
            time_taken = finish - self.start
            self.route.append((direction,  .8 * time_taken))
            #mirrored_route = [(opposite, time_taken)] + self.mirrored_route  #this will be the mirror of the route we just took
        if key == keybd.Key.esc:
            # Stop listener
            return False


    def __init__(self):
        super().__init__()
        self.initUI()
        self.state_left = win32api.GetKeyState(0x01)
        self.check_black = (1058, 670)  #this is a pixel on the lower screen we are going to check if it turns black
        self.up = win32con.VK_UP
        self.down = win32con.VK_DOWN
        self.left = win32con.VK_LEFT
        self.right = win32con.VK_RIGHT
        self.keyboard = Controller()
        self.PP = 5
        self.route = []
        self.mirrored_route = []
        self.prev_key = None
        self.listener = None


    def battled(self):
        self.PP = self.PP - 1

    def keypress(self, key):
        time.sleep(.2)
        self.keyboard.press(key)
        time.sleep(.1)
        self.keyboard.release(key)
        time.sleep(.2)

    def check_poke(self):
        self.keypress('a')
        self.keypress(Key.down)
        self.keypress(Key.down)
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

    def pickup(self):
        time.sleep(1)
        self.keypress('z')
        self.keyboard.press('a')
        time.sleep(.3)
        self.keyboard.release('a')
        time.sleep(.7)
        self.keypress(Key.down)
        self.check_poke()
        self.keypress(Key.down)
        self.check_poke()
        self.keypress(Key.right)
        self.check_poke()
        self.keypress(Key.up)
        self.check_poke()
        time.sleep(.5)
        self.keypress('z')
        time.sleep(4)

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

    def battle_flee(self):
        time.sleep(6)
        self.keypress(Key.down)
        self.keypress(Key.right)
        self.keyboard.press('a')
        time.sleep(.1)
        self.keyboard.release('a')
        time.sleep(5)

    def walk(self, direction, dur,
             battle):  # here we set the direction we want to walk in, the time we walk here, and if we battle or not
        win32api.keybd_event(direction, 0, 0, 0)
        stop = time.time() + dur
        while time.time() < stop:
            time.sleep(.01)
            if self.screen_change():
                time.sleep(.3)
                win32api.keybd_event(direction, 0, win32con.KEYEVENTF_KEYUP, 0)
                time.sleep(.2)
                self.battle_attack() if battle else print("hi")
            win32api.keybd_event(direction, 0, 0, 0)
        win32api.keybd_event(direction, 0, win32con.KEYEVENTF_KEYUP, 0)





    def initUI(self):
        #create buttons and their event handler
        pickBtn = QPushButton('Run Pickup', self)
        pickBtn.setCheckable(True)
        pickBtn.move(10, 10)
        pickBtn.clicked[bool].connect(self.handleBtn)

        routingBtn = QPushButton('Run Route', self)
        routingBtn.setCheckable(True)
        routingBtn.move(10, 60)
        routingBtn.clicked[bool].connect(self.handleBtn)

        RecordBtn = QPushButton('Record Route', self)
        RecordBtn.setCheckable(True)
        RecordBtn.move(10, 110)
        RecordBtn.clicked[bool].connect(self.handleBtn)

        routeBtn = QPushButton('Show Route', self)
        routeBtn.setCheckable(True)
        routeBtn.move(10, 160)
        routeBtn.clicked[bool].connect(self.handleBtn)

        clearBtn = QPushButton('Clear Route', self)
        clearBtn.setCheckable(True)
        clearBtn.move(10, 210)
        clearBtn.clicked[bool].connect(self.handleBtn)

        healBtn = QPushButton('Poke Center', self)
        healBtn.setCheckable(True)
        healBtn.move(10, 210)
        healBtn.clicked[bool].connect(self.handleBtn)


        self.setGeometry(300, 300, 650, 400)
        self.setWindowTitle('Poke Bot')
        self.show()

    # def mousePressEvent(self, QMouseEvent):
    #
    #     print(QMouseEvent.pos())

    def run_route(self):
        time.sleep(2)
        for r in self.route:
            time.sleep(.1)
            self.walk(r[0], r[1], 1)

    def pokeCenter(self):
        self.walk(self.up, 3, 1)
        time.sleep(.2)
        self.walk(self.right, 3, 1)
        time.sleep(.2)
        self.walk(self.up, 3, 1)
        time.sleep(.2)
        self.walk(self.left, 3, 1)
        time.sleep(.2)
        self.walk(self.up, 2, 1)
        time.sleep(.2)
        self.walk(self.left, .4, 1)
        time.sleep(.2)
        self.walk(self.up, 1, 1)
        time.sleep(.2)
        self.walk(self.left, .75, 1)
        time.sleep(.2)
        self.walk(self.up, 4, 1)
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
        self.walk(self.down, 2, 1, )
        time.sleep(.1)
        self.walk(self.right, .6, 1)
        time.sleep(.1)
        self.walk(self.down, 4, 1)
        self.walk(self.left, .85, 1)

    def handleBtn(self):

        source = self.sender()

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

    def onActivated(self, text):
        self.genreLbl.setText(text)
        self.genreLbl.adjustSize()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ReportExample()
    sys.exit(app.exec_())