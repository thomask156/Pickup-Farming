import win32api, win32gui
import pyscreenshot as ImageGrab
import time

# width = win32api.GetSystemMetrics(0)
# height = win32api.GetSystemMetrics(1)
# midWidth = int((width + 1) / 2)
# midHeight = int((height + 1) / 2)
#
# state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
# while True:
#     a = win32api.GetKeyState(0x01)
#     if a != state_left:  # Button state changed
#         state_left = a
#         print(a)
#         if a < 0:
#             print('Left Button Pressed')
#         else:
#             print('Left Button Released')
#     time.sleep(0.001)

# check_black = (1090, 646)
#
# def get_pixel_colour(i_x, i_y):
#     i_desktop_window_id = win32gui.GetDesktopWindow()
#     i_desktop_window_dc = win32gui.GetWindowDC(i_desktop_window_id)
#     long_colour = win32gui.GetPixel(i_desktop_window_dc, i_x, i_y)
#     i_colour = int(long_colour)
#     return (i_colour & 0xff), ((i_colour >> 8) & 0xff), ((i_colour >> 16) & 0xff)
#
# def screen_change():
#     if get_pixel_colour(check_black[0], check_black[1]) == (0, 0, 0):
#         print("Lower Screen is Black")
#
# screen_change()


# im=ImageGrab.grab()
# im.show()

# part of the screen

if __name__ == '__main__':
    time.sleep(5)
    for i in range(5):
        im=ImageGrab.grab(bbox=(750,646,751,647))
        im.show()
        im = ImageGrab.grab(bbox=(760, 646, 761, 647))
        im.show()
