from math import floor
def aqi(pm2):
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

def calculate(pm2, cLow, cHigh, iLow, iHigh):
    return floor((((iHigh - iLow) / (cHigh - cLow)) * (pm2 - cLow)) + iLow)