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

while True:
    time.sleep(1)

    try:
        aqdata = pm25.read()
        next_value = f'Realtime 2.5 AQI\n{aqdata["pm25 standard"]}'
        if next_value != prev_value:
            if displayReady:
                sio.write(f'Realtime 2.5 AQI\n{aqdata["pm25 standard"]}')
                sio.flush()
            clear()
            print(f'Realtime 2.5 AQI\n{aqdata["pm25 standard"]}')
        prev_value = next_value
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue

   
