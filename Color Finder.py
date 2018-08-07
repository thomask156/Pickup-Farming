import win32gui
import win32api
import time

def get_pixel_colour(i_x, i_y):
    i_desktop_window_id = win32gui.GetDesktopWindow()
    i_desktop_window_dc = win32gui.GetWindowDC(i_desktop_window_id)
    long_colour = win32gui.GetPixel(i_desktop_window_dc, i_x, i_y)
    i_colour = int(long_colour)
    return (i_colour & 0xff), ((i_colour >> 8) & 0xff), ((i_colour >> 16) & 0xff)

x=0
y=0
state_left = win32api.GetKeyState(0x01)
check_black=(1058,670)

while True:
    a = win32api.GetKeyState(0x01)
    if a != state_left and a < 0 :  # Button state changed and is not a key release
        mouse = win32gui.GetCursorPos()
        print(mouse)
        state_left = a #this is the state that we just came from
        x = mouse[0]
        y = mouse[1]
        # if get_pixel_colour(check_black[0], check_black[1]) is (0, 0, 0):
        #     print("Lower Screen is Black")
        # if a < 0:
        #     print('Left Button Pressed')
        # else:
        #     print('Left Button Released')
        print(get_pixel_colour(x, y))

    time.sleep(0.001)


# print(get_pixel_colour(x,y))
# print(get_pixel_colour(1358,64))
# print(win32gui.GetCursorPos())