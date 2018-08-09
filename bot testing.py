from multiprocessing import freeze_support

from pynput.keyboard import Key, Controller
import win32con, win32api, win32gui
import pyscreenshot as ImageGrab
import time
from pynput import keyboard as keybd

up = win32con.VK_UP
down = win32con.VK_DOWN
left = win32con.VK_LEFT
right = win32con.VK_RIGHT

keyboard = Controller()

def get_pixel_color():
    im = ImageGrab.grab(bbox=(750, 646, 751, 647))
    rgb_im = im.convert('RGB')
    r, g, b = rgb_im.getpixel((0, 0))
    return r,g,b


 # need to use somehting other than get pixel color as it is currently
 # thinking of using pyscreenshot on a small area of the screen (1x1 lol) and then checking that value

def screen_change():
    color = get_pixel_color()[:]
    for pixel in color:
        if pixel is not 0:
            return False
    else:
        return True
    return


def keypress(key):
    keyboard.press(key)
    time.sleep(.1)
    keyboard.release(key)
    time.sleep(.1)

def check_poke():
    keypress('a')
    keypress(Key.down)
    keypress(Key.down)
    keypress(Key.down)
    keypress('a')
    keypress(Key.down)
    keyboard.press('a')
    time.sleep(.3)
    keyboard.release('a')
    time.sleep(.3)
    keyboard.press('a')
    time.sleep(.3)
    keyboard.release('a')

def pickup():
    time.sleep(1)
    keypress('z')
    keyboard.press('a')
    time.sleep(.1)
    keyboard.release('a')
    time.sleep(.7)
    keypress(Key.down)
    check_poke()
    keypress(Key.down)
    check_poke()
    keypress(Key.right)
    check_poke()
    keypress(Key.up)
    check_poke()
    time.sleep(.5)
    keypress('z')
    time.sleep(4)

def battle_attack():
    time.sleep(5)
    keyboard.press('a')
    time.sleep(.1)
    keyboard.release('a')
    time.sleep(.5)
    keyboard.press('a')
    time.sleep(.3)
    keyboard.release('a')
    time.sleep(7)
    time.sleep(.3)
    pickup()




def walk(direction, dur, battle):  # here we set the direction we want to walk in, the time we walk here, and if we battle or not
    win32api.keybd_event(direction, 0, 0, 0)
    stop = time.time() + dur
    while time.time() < stop:
        time.sleep(.01)
        if screen_change():
            time.sleep(.3)
            win32api.keybd_event(direction, 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(.2)
            battle_attack() if battle else print("hi")
        win32api.keybd_event(direction, 0, 0, 0)
    win32api.keybd_event(direction, 0, win32con.KEYEVENTF_KEYUP, 0)

if __name__ == '__main__':
    freeze_support()
    time.sleep(1)
    #battle_attack()
    while True:
        walk(up, 1, 1)
        time.sleep(.2)
        walk(down, 3, 1)
        time.sleep(.2)
