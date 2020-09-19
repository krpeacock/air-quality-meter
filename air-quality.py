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
from aqi import aqi25
from aqi import aqi10

def clear(): return 

reset_pin = None

# Create library object, use 'slow' 100KHz frequency!
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
# Connect to a PM2.5 sensor over I2C
pm25 = adafruit_pm25.PM25_I2C(i2c, reset_pin)

print("Found PM2.5 sensor, reading data...")

displayReady = False

with open('/home/kyle/air-quality-meter/config.json') as f:
  data = json.load(f)
  if not data.get('serial'):
    print('Warning - serial port not configured.\nProceeding without display')

  else:
    
    arduino = serial.Serial(data.get('serial'), 9600,
                            timeout=0, parity=serial.PARITY_EVEN, rtscts=1)
    sio = io.TextIOWrapper(io.BufferedRWPair(arduino, arduino))
    time.sleep(2)
    displayReady = True

    last_code = ''

prev_value = ''
values_25 = []
values_10 = []

while True:
    time.sleep(.35)

    try:
        aqdata = pm25.read()
        values_25.insert(0, aqdata["pm25 standard"])
        values_25 = values_25[0:30]
        values_10.insert(0, aqdata["pm10 standard"])
        values_10 = values_10[0:30]

        next_25 = f'{aqi25(math.floor(sum(values_25) / len(values_25)))}'
        next_10 = f'{aqi10(math.floor(sum(values_10) / len(values_10)))}'
        maxAQI = max(next_25, next_10)

        if displayReady:
            sio.write(f'D{maxAQI},${next_25},{next_10}')
            sio.flush()
        clear()
        print(f'Max AQI\n{maxAQI}')
        print(f'Average 2.5 AQI\n{next_25}')
        print(f'Average 10 AQI\n{next_10}')
        print(f'Data Points: {len(values_25)}')
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue


   
