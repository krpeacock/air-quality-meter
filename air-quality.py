# pylint: disable=unused-import
import time
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
import adafruit_pm25
import json
import serial
import io
import json
import os
import math
from aqi import aqi

def clear(): return os.system('clear')

reset_pin = None

# Create library object, use 'slow' 100KHz frequency!
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
# Connect to a PM2.5 sensor over I2C
pm25 = adafruit_pm25.PM25_I2C(i2c, reset_pin)

print("Found PM2.5 sensor, reading data...")

displayReady = False

with open('config.json') as f:
  data = json.load(f)
  if not data.get('serial'):
    print('Warning - serial port not configured.\nProceeding without display')

  else:
    
    arduino = serial.Serial('/dev/ttyACM0', 9600,
                            timeout=0, parity=serial.PARITY_EVEN, rtscts=1)
    sio = io.TextIOWrapper(io.BufferedRWPair(arduino, arduino))
    time.sleep(2)
    displayReady = True

    last_code = ''

prev_value = ''
all_values = []

while True:
    time.sleep(1)

    try:
        aqdata = pm25.read()
        all_values.insert(0, aqdata["pm25 standard"])
        all_values = all_values[0:30]
        next_value = f'{math.floor(sum(all_values) / len(all_values))}'
        if next_value != prev_value:
            if displayReady:
                sio.write(next_value)
                sio.flush()
            clear()
            print(f'Average 2.5 AQI\n{next_value}')
            print(f'Data Points: {len(all_values)}')
        prev_value = next_value
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue


   
