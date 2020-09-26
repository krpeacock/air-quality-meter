# pylint: disable=unused-import
import time
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
import neopixel
import adafruit_pm25
import json
import serial
import io
import json
import os
import math
from aqi import aqi25
from aqi import aqi10


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 30

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.RGB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

pixels.fill((8, 146, 208))


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

prev_out = ''
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

        if int(maxAQI) < 50:
          pixels.fill((0, 228, 1))

        out = f'{maxAQI},{next_25},{next_10}\n'

        if displayReady:
            if out != prev_out:
              sio.write(out)
              prev_out = out
            sio.flush()
        clear()
        print(f'Max AQI\n{maxAQI}')
        print(f'Average 2.5 AQI\n{next_25}')
        print(f'Average 10 AQI\n{next_10}')
        print(f'Data Points: {len(values_25)}')
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue


   
