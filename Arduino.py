import serial
import time
import io
import os
def clear(): return os.system('clear')


arduino = serial.Serial('/dev/cu.usbmodem14201', 9600,
                        timeout=0, parity=serial.PARITY_EVEN, rtscts=1)
sio = io.TextIOWrapper(io.BufferedRWPair(arduino, arduino))
time.sleep(2)

last_code = ''


def compare_input(code):
    global last_code
    if code == last_code:
        return
    last_code = code
    switcher = {
        '0': 'RIGHT',
        '1': 'UP',
        '2': 'DOWN',
        '3': 'LEFT',
        '4': 'SELECT',
    }

    msg = switcher.get(code, 'NONE')
    clear()
    print('Displayed Text')
    print('----------------')
    print(f'Button: {msg}\nhi')
    print('----------------')
    sio.write(f'Button: {msg}\nhi')
    sio.flush()


while True:
    new_message = bytes(arduino.readline()).decode("utf-8", 'ignore')
    if(new_message != ''):
        compare_input(new_message)
    time.sleep(.1)
