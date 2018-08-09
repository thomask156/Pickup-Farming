import sys
import win32api, win32gui, win32con
import time
import pyscreenshot as ImageGrab

from pynput.keyboard import Key, Controller
from pynput import keyboard as keybd
from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QApplication, QLabel)
from PyQt5.QtWidgets import QTableView, QComboBox


class ReportExample(QWidget):

    def keyPressEvent(self, key):
        print("it's working")
        if self.prev_key is not key:
            prev_key = key
            self.start = time.time()
        # if prev_key is not key:
        #     prev_key = key


    def convertDir(self, direction):
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

    def keyPressRelease(self, key):
        finish = time.time()
        direction, opposite= self.convertDir(str(key)[4:])
        if direction != "you're mom gay":
            time_taken = finish - self.start
            self.route.append((direction, time_taken))
            self.mirrored_route = [(opposite, time_taken)] + self.mirrored_route  #this will be the mirror of the route we just took
        if key == keybd.Key.esc:
            # Stop listener
            self.close()


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
        self.PP = 3
        self.route = []
        self.mirrored_route = []
        self.prev_key = None


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

    def battled(self):
        global PP
        PP -= 1

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
        print("opening menu")
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
        #self.battled()
        time.sleep(7)
        time.sleep(.3)
        self.pickup()
        #return

    def battle_flee(self):
        time.sleep(6)
        print("running away")
        self.keypress(Key.down)
        self.keypress(Key.right)
        self.keyboard.press('a')
        time.sleep(.1)
        self.keyboard.release('a')
        time.sleep(5)
        #return

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
        allCustBtn = QPushButton('Run Pickup', self)
        allCustBtn.setCheckable(True)
        allCustBtn.move(10, 10)
        allCustBtn.clicked[bool].connect(self.handleBtn)

        allGenresBtn = QPushButton('Run Route', self)
        allGenresBtn.setCheckable(True)
        allGenresBtn.move(10, 60)
        allGenresBtn.clicked[bool].connect(self.handleBtn)

        clearBtn = QPushButton('Testing', self)
        clearBtn.setCheckable(True)
        clearBtn.move(10, 110)
        clearBtn.clicked[bool].connect(self.handleBtn)


        self.setGeometry(300, 300, 650, 400)
        self.setWindowTitle('Poke Bot')
        self.show()

    # def mousePressEvent(self, QMouseEvent):
    #
    #     print(QMouseEvent.pos())

    def run_route(self):
        time.sleep(2)
        while self.PP > 0:
            time.sleep(.1)
            self.walk(self.down, 1, True)
            time.sleep(.1)
            self.walk(self.up, 1, True)


    def handleBtn(self):

        source = self.sender()

        if source.text() == "Run Pickup":
            # TODO: make the calls to run the appropriate query and get the model
            print("starting to pick up")
            self.pickup()
        if source.text() == "Run Route":
            # TODO: make the calls to run the appropriate query and get the model
            self.run_route()
        elif source.text() == "Testing":
                self.battle_attack()

    def onActivated(self, text):
        self.genreLbl.setText(text)
        self.genreLbl.adjustSize()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ReportExample()
    sys.exit(app.exec_())