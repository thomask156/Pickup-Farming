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
from PyQt5 import Qt
from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QApplication, QLabel)
from PyQt5.uic.properties import QtGui
from PyQt5 import QtCore
import sys
from QTGui import *
from PyQt5.QtWidgets import QTableView, QComboBox


class ReportExample(QWidget):
    def __init__(self):
        super().__init__()
        self.installEventFilter(self)
        self.initUI()
        self.grabKeyboard()


    def initUI(self):

        #create buttons and their event handler
        allCustBtn = QPushButton('Testing', self)
        allCustBtn.setCheckable(True)
        allCustBtn.move(10, 10)
        allCustBtn.clicked[bool].connect(self.handleBtn)
        self.default_genre = "Metal"
        self.genreLbl = QLabel(self.default_genre, self)
        self.genreLbl.move(200, 60)
        self.setGeometry(300, 300, 650, 400)
        self.setWindowTitle('Reports')
        self.show()
        self.keyPressEvent = self.keyPressEvent
        self.keyReleaseEvent = self.keyReleaseEvent
        self.start = 0
        self.prev_key = None


    def handleBtn(self):

        source = self.sender()

        if source.text() == "Testing":
            # TODO: make the calls to run the appropriate query and get the model
            print("stuff")


    def onActivated(self, text):
        self.genreLbl.setText(text)
        self.genreLbl.adjustSize()

    # def keyPressEvent(self, event):
    #     print(str(event.key()))
    #     print()

    def eventFilter(self, source, event):  #this will be used for recording key presses

        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() != self.prev_key:   #this is because this thing likes to say I pressed something multiple times when holding down a key
                #print(str(self.prev_key))
                self.prev_key = event.key()
                #print(str(event.key()))
                self.start = time.time()
                #print(self.start)
        if event.type() == QtCore.QEvent.KeyRelease:
            if self.start is not 0:
                if not event.isAutoRepeat():  #this is for the same reason as above, but doesn't help arrow keys
                    print(str(event.key())+" was held for "+str(time.time()-self.start)+" seconds")
                    self.prev_key = None

        return super(ReportExample, self).eventFilter(source, event)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ReportExample()
    sys.exit(app.exec_())
