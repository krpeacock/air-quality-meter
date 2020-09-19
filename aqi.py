from math import floor
def aqi25(pm2):
    if pm2 <= 12:
        return calculate(pm2, 0, 12, 0, 50)
    if pm2 > 12 and pm2 <=35.4:
        return calculate(pm2, 12.1, 35.4, 51, 100)
    if pm2 > 35.4 and pm2 <= 55.4:
        return calculate(pm2, 35.5, 55.4, 101, 150)
    if pm2 > 55.4 and pm2 <= 150.4:
        return calculate(pm2, 55.4, 150.4, 151, 200)
    if pm2 > 150.4 and pm2 <= 250.5:
        return calculate(pm2, 150.4, 250.5, 201, 300)
    if pm2 > 250.4 and pm2 <= 350.5:
        return calculate(pm2, 250.4, 350.5, 301, 400)
    if pm2 > 350.4 and pm2 <= 500.4:
        return calculate(pm2, 350.4, 500.4, 401, 500)
    
def aqi10(pm10):
    if(pm10 <= 54):
        return calculate(pm10, 0, 54, 0, 50)
    if pm10 > 54 and pm10 < 155:
        return calculate(pm10, 55, 154, 51, 100)
    if pm10 >= 155 and pm10 < 255:
        return calculate(pm10, 155, 254, 101, 150)
    if pm10 >= 255 and pm10 < 355:
        return calculate(pm10, 255, 354, 151, 200)
    if pm10 >= 355 and pm10 < 425:
        return calculate(pm10, 355, 424, 201, 300)
    if pm10 >= 425 and pm10 < 505:
        return calculate(pm10, 425, 504, 301, 400)
    if pm10 >= 505 and pm10 < 605:
        return calculate(pm10, 505, 604, 401, 500)

def calculate(pm, cLow, cHigh, iLow, iHigh):
    return floor((((iHigh - iLow) / (cHigh - cLow)) * (pm - cLow)) + iLow)