import pyautogui
import time
from pynput.mouse import Listener

stop_loop = False

def on_click(x, y, button, pressed):
    global stop_loop
    if pressed:
        stop_loop = True


listener = Listener(on_click=on_click)
listener.start()

try:
    while not stop_loop:
        print('test')
        x, y = pyautogui.position()
        position_str = f'X: {x:4} Y: {y:4}'
        print(position_str)
        time.sleep(0.1)
except KeyboardInterrupt:
    print('\nStopped by keyboard interruption.')
except Exception as e:
    print(f'\nAn error occurred: {e}')
finally:
    listener.stop()
    print('Done.')
