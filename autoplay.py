from pynput.keyboard import Key, Controller
import win32con, win32api, win32gui
import pyscreenshot as ImageGrab
import time
from pynput import keyboard as keybd  #we have to do this because everything wants to be called keyboard apparently lol

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
    PP = 3

    def battled():
        global PP
        PP -= 1
        return None

    def keypress(key):
        keyboard.press(key)
        time.sleep(.2)
        keyboard.release(key)
        time.sleep(.2)

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
        print("opening menu")
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
        print("fight time")
        keyboard.press('a')
        time.sleep(.3)
        keyboard.release('a')
        time.sleep(.5)
        keyboard.press('a')
        time.sleep(.3)
        keyboard.release('a')
        battled()
        time.sleep(7)
        time.sleep(.3)
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
            time.sleep(0.1)
            if screen_change():
                print("now it should fight")
                time.sleep(.1)
                win32api.keybd_event(direction, 0, win32con.KEYEVENTF_KEYUP, 0)
                battle_attack() if battle else battle_flee()
                #win32api.keybd_event(direction, 0, 0, 0)
            win32api.keybd_event(direction, 0, 0, 0)
        win32api.keybd_event(direction, 0, win32con.KEYEVENTF_KEYUP, 0)

    def restore():
        walk(up, .001, False)
        walk(right, .08, False)
        walk(up, .1, False)
        walk(left, .1, False)
        walk(up, 1.3, False)
        return None
    restore()
    route = []
    mirrored_route = [] #the reverse of the route, we need to mirror their route to make a circuit, also kys for reading this
    prev_key = None
    start = 0
    finish = 0

    def on_press(key):
        print("test")
        global prev_key
        global start
        if prev_key is not key:
            prev_key = key
            start = time.time()
        # if prev_key is not key:
        #     prev_key = key


    def convert(direction):
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

    def on_release(key):
        global prev_key
        global finish, start
        global mirrored_route
        finish = time.time()
        direction, opposite= convert(str(key)[4:])
        if direction != "you're mom gay":
            time_taken = finish - start
            route.append((direction, time_taken))
            mirrored_route = [(opposite, time_taken)] + mirrored_route  #this will be the mirror of the route we just took
        if key == keybd.Key.esc:
            # Stop listener
            return False

    # Collect events until released

    # with keybd.Listener(
    #         on_press=on_press,
    #         on_release=on_release) as listener:
    #     listener.join()
    #listener.start()

    #time.sleep(3)
    #listener.start()

    # def create_route():
    #     global route, mirrored_route
    #     print("Now creating route, please move to the end of the path you want to walk up and down")
    #     listener.start()
    #     route += mirrored_route
    #     return

    #create_route()
    #time.sleep(2)
    # while PP > 0:
    #     # for inst in route:
    #     #     #print(str(inst[0]))
    #     #     walk(inst[0], inst[1], 0)
    #     if PP is 1:
    #         restore()
    #     walk(down, 1, True)
    #     time.sleep(.1)
    #     walk(up, 1, True)



