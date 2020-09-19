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
25_values = []
10_values = []

while True:
    time.sleep(1)

    try:
        aqdata = pm25.read()
        25_values.insert(0, aqdata["pm25 standard"])
        25_values = 25_values[0:30]
        10_values.insert(0, aqdata["pm10 standard"])
        10_values = 10_values[0:30]


        next_25 = f'{math.floor(sum(25_values) / len(25_values))}'
        next_10 = f'{math.floor(sum(10_values) / len(10_values))}'
        maxAQI = max(next_25, next_10)

        if displayReady:
            sio.write(f'D{maxAQI},${next_25},{next_10}')
            sio.flush()
        clear()
        print(f'Max AQI\n{maxAQI}')
        print(f'Average 2.5 AQI\n{next_25}')
        print(f'Average 10 AQI\n{next_10}')
        print(f'Data Points: {len(25_values)}')
        prev_value = next_value
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue


   
