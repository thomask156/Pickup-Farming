from pynput.keyboard import Key, Controller
import win32con, win32api, win32gui
import pyscreenshot as ImageGrab
import time

# trying to make it so that it can simulate pressing and holding down a key
# I think that i  might need to use something besides pynput, as I can't find a hold function
# something to do with win32 could work, as it has win32.keyb_event which might be something to look into later

keyboard = Controller()
# time.sleep(2)
# time.sleep(2)
# keyboard.press(Key.down)
# time.sleep(2)
# keyboard.release(Key.down)

time.sleep(5)

up = win32con.VK_UP
down = win32con.VK_DOWN
left = win32con.VK_LEFT
right = win32con.VK_RIGHT

check_black = (1090, 646)

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

if __name__ == '__main__':

    time.sleep(1.5) #this is to give me time to transition to citra, AKA clicking it and making it fullscreen
    global PP
    PP = 2

    def battled():
        PP -= 1
        return None

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
        time.sleep(.3)
        keypress('z')
        keyboard.press('a')
        time.sleep(.3)
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
        time.sleep(.3)
        keyboard.release('a')
        time.sleep(.5)
        keyboard.press('a')
        time.sleep(.3)
        keyboard.release('a')
        #battled()
        time.sleep(7)
        print("picking up now")
        time.sleep(.1)
        pickup()
        return

    def battle_flee():
        time.sleep(6)
        print("running away")
        keypress(Key.down)
        keypress(Key.right)
        keyboard.press('a')
        time.sleep(.1)
        keyboard.release('a')
        time.sleep(5)
        return

    def walk(direction, dur,  battle):  #here we set the direction we want to walk in, the time we walk here, and if we battle or not
        win32api.keybd_event(direction, 0, 0, 0)
        stop = time.time() + dur
        while time.time() < stop:
            time.sleep(0.01)
            if screen_change():
                print("now it should run away")
                battle_attack() if battle else battle_flee()
            win32api.keybd_event(direction, 0, 0, 0)
        win32api.keybd_event(direction, 0, win32con.KEYEVENTF_KEYUP, 0)

    def restore():
            return None

    battle_attack()
    #pickup()
    # while PP > 0:
    #     walk(down, 1, False)
    #     walk(up, 1, False)


