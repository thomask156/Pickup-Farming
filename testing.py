# import win32api, win32gui
# import pyscreenshot as ImageGrab
# import time
# import timer
# from pynput.keyboard import Key, Controller
# import win32con
#
# # width = win32api.GetSystemMetrics(0)
# # height = win32api.GetSystemMetrics(1)
# # midWidth = int((width + 1) / 2)
# # midHeight = int((height + 1) / 2)
# #
# # state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
# # while True:
# #     a = win32api.GetKeyState(0x01)
# #     if a != state_left:  # Button state changed
# #         state_left = a
# #         print(a)
# #         if a < 0:
# #             print('Left Button Pressed')
# #         else:
# #             print('Left Button Released')
# #     time.sleep(0.001)
#
# # check_black = (1090, 646)
# #
# # def get_pixel_colour(i_x, i_y):
# #     i_desktop_window_id = win32gui.GetDesktopWindow()
# #     i_desktop_window_dc = win32gui.GetWindowDC(i_desktop_window_id)
# #     long_colour = win32gui.GetPixel(i_desktop_window_dc, i_x, i_y)
# #     i_colour = int(long_colour)
# #     return (i_colour & 0xff), ((i_colour >> 8) & 0xff), ((i_colour >> 16) & 0xff)
# #
# # def screen_change():
# #     if get_pixel_colour(check_black[0], check_black[1]) == (0, 0, 0):
# #         print("Lower Screen is Black")
# #
# # screen_change()
#
#
# # im=ImageGrab.grab()
# # im.show()
#
# # part of the screen
#
# if __name__ == '__main__':
#     # global power
#     # power = 5
#     # time.sleep(5)
#     # def set_power():
#     #     global power
#     #     power -= 1
#     #
#     # print(power)
#     # set_power()
#     # print(power)
#     # # for i in range(5):
#     # #     im=ImageGrab.grab(bbox=(750,646,751,647))
#     # #     im.show()
#     # #     im = ImageGrab.grab(bbox=(760, 646, 761, 647))
#     # #     im.show()
#
#
#
#     from pynput import keyboard as keybd
#     keyboard = Controller()
#     route = []
#     mirrored_route = [] #the reverse of the route, we need to mirror their route to make a circuit, also kys for reading this
#     prev_key = None
#     start = 0
#     finish = 0
#
#     def on_press(key):
#         global prev_key
#         global start
#         if prev_key is not key:
#             prev_key = key
#             start = time.time()
#         # if prev_key is not key:
#         #     prev_key = key
#
#
#     def convert(direction):
#         up = win32con.VK_UP
#         down = win32con.VK_DOWN
#         left = win32con.VK_LEFT
#         right = win32con.VK_RIGHT
#         if direction == "down":
#             return down, up
#         if direction == "up":
#             return up, down
#         if direction == "left":
#             return left, right
#         if direction == "right":
#             return right, left
#         return "you're mom gay", "no u"
#
#     def on_release(key):
#         global prev_key
#         global finish, start
#         global mirrored_route
#         finish = time.time()
#         direction, opposite= convert(str(key)[4:])
#         if direction != "you're mom gay":
#             time_taken = finish - start
#             route.append((direction, time_taken))
#             mirrored_route = [(opposite, time_taken)] + mirrored_route  #this will be the mirror of the route we just took
#         if key == keybd.Key.esc:
#             # Stop listener
#             return False
#
#     # Collect events until released
#     with keybd.Listener(
#             on_press=on_press,
#             on_release=on_release) as listener:
#         listener.join()
#
#     #print(route)
#     #print(str(route.__getitem__(0)[0])[4:])
#     #route+mirrored_route
#
#     def get_pixel_color():
#         im = ImageGrab.grab(bbox=(750, 646, 751, 647))
#         rgb_im = im.convert('RGB')
#         r, g, b = rgb_im.getpixel((0, 0))
#         return r, g, b
#
#
#     # need to use somehting other than get pixel color as it is currently
#     # thinking of using pyscreenshot on a small area of the screen (1x1 lol) and then checking that value
#
#     def screen_change():
#         color = get_pixel_color()[:]
#         for pixel in color:
#             if pixel is not 0:
#                 return False
#         else:
#             return True
#         return
#
#
#     def keypress(key):
#         keyboard.press(key)
#         time.sleep(.2)
#         keyboard.release(key)
#         time.sleep(.2)
#
#     def battle_flee():
#         time.sleep(6)
#         keypress(Key.down)
#         keypress(Key.right)
#         keyboard.press('a')
#         time.sleep(.1)
#         keyboard.release('a')
#         time.sleep(5)
#         return
#
#
#
#     def walk(direction, dur,  battle):  #here we set the direction we want to walk in, the time we walk here, and if we battle or not
#         win32api.keybd_event(direction, 0, 0, 0)
#         stop = time.time() + dur
#         while time.time() < stop:
#             time.sleep(0.01)
#             if screen_change():
#                 time.sleep(.1)
#                 win32api.keybd_event(direction, 0, win32con.KEYEVENTF_KEYUP, 0)
#                 battle_flee()
#                 #win32api.keybd_event(direction, 0, 0, 0)
#             win32api.keybd_event(direction, 0, 0, 0)
#         win32api.keybd_event(direction, 0, win32con.KEYEVENTF_KEYUP, 0)
#
#     route += mirrored_route
#     while 3>0:
#         for inst in route:
#             #print(str(inst[0]))
#             time.sleep(.3)
#             walk(inst[0], inst[1], 0)


""" An example gui that displays reports based on database queries.
    It used classes from PyQt including a model/view pair as well as a database accessor module.
"""
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QApplication, QLabel, QListWidget, QCheckBox)
from PyQt5.uic.properties import QtGui
from PyQt5 import QtCore
import sys
from QTGui import *
from PyQt5.QtWidgets import QTableView, QComboBox
from pynput.keyboard import Key, Controller
import sys
import win32api, win32gui, win32con
import time
import pyscreenshot as ImageGrab

from pynput.keyboard import Key, Controller
from pynput import keyboard as keybd
from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QApplication, QLabel, QCheckBox)
from PyQt5.QtWidgets import QTableView, QComboBox
from PyQt5 import *


class ReportExample(QWidget):
    def __init__(self):
        super().__init__()
        #self.installEventFilter(self)
        self.initUI()
        self.keyboard = Controller()


    def initUI(self):

        #create buttons and their event handler
        self.setWindowTitle('Poke Bot')

        allCustBtn = QPushButton('Testing', self)
        allCustBtn.setCheckable(True)
        allCustBtn.move(10, 10)
        allCustBtn.clicked[bool].connect(self.handleBtn)

        showRtBtn = QPushButton('Show Route', self)
        showRtBtn.setCheckable(True)
        showRtBtn.move(100, 10)
        showRtBtn.clicked[bool].connect(self.handleBtn)
        self.setGeometry(300, 300, 650, 400)
        for i in range(1,7):
            self.initPickCheckbox(i, 20, 20*i+10)
        for i in range(1,7):
            self.initHMCheckbox("slot "+str(i)+" has HM", 120, 20*i+10)

        self.show()

        self.hasPick = []
        self.hasHM = {}
        for i in range(1,7):
            self.hasHM[str(i)] = False

    def initPickCheckbox(self, name, x, y):
        self.b = QCheckBox(str(name), self)
        self.b.stateChanged.connect(self.clickBox)
        self.b.move(x, y)
        self.b.resize(320, 40)

    def initHMCheckbox(self, name, x, y):
        self.c = QCheckBox(str(name), self)
        #self.c.stateChanged.connect(self.HMclickBox)
        self.c.move(x, y)
        self.c.resize(320, 40)

    def clickBox(self, state):
        source = self.sender()
        print(QtCore.Qt.Checked)
        # if state == QtCore.Qt.Checked:
        #     for i in range(1, 7):
        #         if source.text() == str(i):
        #             self.hasPick.append(i)
    #     else:
    #         for i in range(1,7):
    #             if source.text() == str(i):
    #                 self.hasPick.remove(i)
    #
    # def HMclickBox(self, state):
    #     source = self.sender()
    #     if state == QtCore.Qt.Checked:
    #         for i in range(1, 7):
    #             if source.text()[5] == str(i):
    #                 #have i as the key, have it set to true here
    #                 self.hasHM[str(i)] = True
    #     else:
    #         for i in range(1, 7):
    #             if source.text()[5] == str(i):
    #                 self.hasHM[str(i)] = False

    def handleBtn(self):

        source = self.sender()

        if source.text() == "Testing":
            # TODO: make the calls to run the appropriate query and get the model

            print(self.hasHM)
        if source.text() == "Show Route":
            print(self.hasPick)
            time.sleep(1)
            #aself.check_poke(False)


    def onActivated(self, text):
        self.genreLbl.setText(text)
        self.genreLbl.adjustSize()


    # def keypress(self, key):
    #     time.sleep(.2)
    #     self.keyboard.press(key)
    #     time.sleep(.1)
    #     self.keyboard.release(key)
    #     time.sleep(.2)
    #
    # def check_poke(self, hasHM):
    #     self.keypress('a')
    #     self.keypress(Key.down)
    #     self.keypress(Key.down)
    #     if hasHM:
    #         self.keypress(Key.down)
    #     self.keypress('a')
    #     self.keypress(Key.down)
    #     self.keyboard.press('a')
    #     time.sleep(.3)
    #     self.keyboard.release('a')
    #     time.sleep(.3)
    #     self.keyboard.press('a')
    #     time.sleep(.3)
    #     self.keyboard.release('a')
    #
    # def move_to(self, fron, to): #supposed to be to and from but python said no
    #     if fron is to:
    #         return
    #     elif fron % 2 == to % 2:
    #         steps = int((to-fron)/2)
    #         for i in range(steps):
    #             time.sleep(.1)
    #             self.keypress(Key.down)
    #     else:
    #         self.keypress(Key.right)
    #         steps = int((to - (fron+1)) / 2)
    #         for i in range(steps):
    #             time.sleep(.1)
    #             self.keypress(Key.down)

    # def pickup(self):
    #     #check each slot that was selected
    #
    #     time.sleep(1)
    #     self.keypress('z')
    #     self.keyboard.press('a')
    #     time.sleep(.3)
    #     self.keyboard.release('a')
    #     time.sleep(.7)
    #     time.sleep(1.5)
    #     size = self.hasPick.__len__()
    #     if size is not 0:
    #         self.hasPick.sort()
    #         self.move_to(1, self.hasPick[0])
    #         for i in range(0, size):
    #             self.check_poke(self.hasHM[str(self.hasPick[i])])
    #             if i < size - 1:
    #                 self.move_to(self.hasPick[i], self.hasPick[i + 1])
    #     self.keypress('z')
    #     time.sleep(4)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ReportExample()
    sys.exit(app.exec_())
