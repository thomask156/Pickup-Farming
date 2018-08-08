from tkinter import *
from pynput.keyboard import Key, Controller
import time
import random
import win32gui, win32api
from PIL import ImageGrab
from pynput import keyboard as keybd






def printHi():
    print("hi")



class Window(Frame):
    keyboard = Controller()

    def keypress(self, key):
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

    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.start = 0
        self.master = master
        self.init_window()
        master.bind('<Return>', self.enterPP)
        self.x = 0
        self.y = 0
        self.state_left = win32api.GetKeyState(0x01)
        self.check_black = (1058, 670)

    def init_window(self):
        self.master.title("Thomas") #this is the title of the window

        self.pack(fill=BOTH, expand=1)

        #self.clickButton = Button(self, text="Click Me", command=self.reflexTest)

        #self.clickButton.place(x=200.0, y=150.0, anchor=CENTER)

        self.buttonPP = Button(self, text="Pickup", command=self.pickup)
        self.buttonPP.pack(side=TOP)


    def nameChange(self):
        self.clickButton.configure(text="Nice Job!", bg="green")

    def setPP(self):
        print(self.entryPP.get())

    def enterPP(self, event=None):
        print(self.entryPP.get())

    def get_pixel_colour(self, i_x, i_y):
        i_desktop_window_id = win32gui.GetDesktopWindow()
        i_desktop_window_dc = win32gui.GetWindowDC(i_desktop_window_id)
        long_colour = win32gui.GetPixel(i_desktop_window_dc, i_x, i_y)
        i_colour = int(long_colour)
        return (i_colour & 0xff), ((i_colour >> 8) & 0xff), ((i_colour >> 16) & 0xff)

    def screenShot(self):
        im=ImageGrab.grab(bbox=(10, 20, 110, 210))
        im.show()




root = Tk()



root.geometry("400x300")

app = Window(root)

root.mainloop()
