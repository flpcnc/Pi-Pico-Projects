from machine import Pin, I2C
from bmp280 import *
import time
import math

bus = I2C(0, scl=Pin(1), sda=Pin(0), freq=200000)
bmp = BMP280(bus)

bmp.use_case(BMP280_CASE_INDOOR)

# Altitude média de São Carlos, SP, em metros (689 metros)
altitude_sao_carlos = 689.0

while True:
    pressure = bmp.pressure
    p_bar = pressure / 100000
    p_mmHg = pressure / 133.322
    temperature = bmp.temperature

    # Convertendo a pressão do sensor para a pressão ao nível do mar em São Carlos-SP
    sea_level_pressure = pressure / math.pow(1 - altitude_sao_carlos / 44330.0, 5.255)

    # Cálculo da altitude com base na pressão ao nível do mar em São Carlos
    altitude = 44330.0 * (1 - math.pow(sea_level_pressure / 101325.0, 1/5.255))

    print("Temperature: {} C".format(temperature))
    print("Pressure: {} Pa, {} bar, {} mmHg".format(pressure, p_bar, p_mmHg))
    print("Altitude: {} meters".format(altitude))
    
    time.sleep(10)

