from machine import Pin, I2C, ADC
import ssd1306
import dht
import utime
from bmp280 import *
import math
from uio import StringIO

# Configuração do display OLED
i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Configuração do sensor DHT11
dht_sensor = dht.DHT11(Pin(22))

# Configuração do sensor BMP280
bus = I2C(0, sda=Pin(0), scl=Pin(1), freq=200000)
bmp = BMP280(bus)
bmp.use_case(BMP280_CASE_INDOOR)

# Altitude média de São Carlos, SP, em metros (689 metros)
altitude_sao_carlos = 689.0

def display_temperature_humidity():
    dht_sensor.measure()
    temperature = dht_sensor.temperature()
    humidity = dht_sensor.humidity()
    
    # Verifica se a leitura da umidade é válida
    if isinstance(temperature, int) and isinstance(humidity, int):
        # Limpa a tela do OLED
        oled.fill(0)
        
        # Escreve "WashSense" na primeira linha
        # oled.text("WashSense", 0, 0)
        
        oled.text("FLPCNC", 0, 0)
        
        # Escreve temperatura e umidade no OLED
        oled.text("Temp: {}C".format(int(temperature)), 0, 16)
        oled.text("Umidade: {}%".format(int(humidity)), 0, 32)
          
        # Atualiza o display
        oled.show()

def read_bmp280_data():
    pressure = bmp.pressure
    p_bar = pressure / 100000
    p_mmHg = round(pressure / 133.322, 2)  # Arredonda para 2 casas decimais
    temperature = bmp.temperature

    # Convertendo a pressão do sensor para a pressão ao nível do mar em São Carlos
    sea_level_pressure = pressure / math.pow(1 - altitude_sao_carlos / 44330.0, 5.255)

    # Cálculo da altitude com base na pressão ao nível do mar em São Carlos
    altitude = int(44330.0 * (1 - math.pow(sea_level_pressure / 101325.0, 1/5.255)))

    return int(temperature), altitude, p_mmHg  # Convertido para int

def display_data_on_oled(tmp1, tmp2, altitude, mmHg, humidity):
    oled.fill(0)
    oled.text("   FLPCNC   ", 0, 0)
    oled.text("T1 {}C T2 {}C".format(tmp1, int(tmp2)), 0, 16)  # Convertido para int
    oled.text("UR: {}% Alt: {}".format(int(humidity), altitude), 0, 32)
    oled.text("mmHg: {:.2f}".format(mmHg), 0, 48)  # Mostra mmHg com 2 casas decimais
    oled.show()

def log_data_to_csv(data):
    with open("data.csv", "a") as file:
        file.write(data)
        file.write("\n")

while True:
    display_temperature_humidity()
    temperature, altitude, mmHg = read_bmp280_data()
    humidity = dht_sensor.humidity()
    
    # Verifica se a leitura da umidade do DHT11 é válida
    if isinstance(humidity, int):
        display_data_on_oled(dht_sensor.temperature(), temperature, altitude, mmHg, humidity)
    
    # Cria uma string com os dados
    data = "{}, {}, {}, {}, {}, {:.2f}".format(
        utime.localtime(),
        dht_sensor.temperature(),
        humidity,
        temperature,
        altitude,
        mmHg
    )
    
    # Log dos dados no arquivo CSV
    log_data_to_csv(data)
    
    serial_data = "Temperature (DHT11): {} C, Umidade (DHT11): {}%, Temperature (BMP280): {} C, Altitude: {} m, mmHg: {:.2f}".format(
        dht_sensor.temperature(), int(humidity), temperature, altitude, mmHg)
    
    print(serial_data)
    
    utime.sleep(15)  # Atraso de 15 segundos entre as leituras

