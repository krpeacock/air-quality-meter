import serial
import json
import time
import io
import random
import math

with open('config.json') as f:
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

sio.write('foo,1,2')
sio.flush()
time.sleep(2)
while True:
    sio.write(f'{random.randint(0, 200)},{random.randint(0, 200)},{random.randint(0, 200)}')
    sio.flush()
    time.sleep(1)