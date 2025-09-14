from machine import Pin, I2C, ADC
import ssd1306
import dht
import utime

# Configuração do display OLED
i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Configuração do sensor DHT11
dht_sensor = dht.DHT11(Pin(22))

# Configuração do sensor interno (ADC)
sensor_temp = ADC(4)
conversion_factor = 3.3 / (65535)

def read_internal_temperature():
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706) / 0.001721
    return temperature

def display_temperature_humidity():
    dht_sensor.measure()
    temperature = dht_sensor.temperature()
    humidity = dht_sensor.humidity()
    
    # Limpa a tela do OLED
    oled.fill(0)
    
    # Escreve "FLPCNC" na primeira linha
    oled.text("     FLPCNC   ", 0, 0)
    
    # Escreve temperatura e umidade no OLED
    oled.text("Temp DHT11: {}C".format(int(temperature)), 0, 16)
    oled.text("Umidade:    {}%".format(humidity), 0, 32)
    
    # Leitura e impressão do sensor de temperatura interno pi pico
    internal_temperature = read_internal_temperature()
    oled.text("T2 Pi Pico: {}C".format(int(internal_temperature)), 0, 48)
    
    # Atualiza o display
    oled.show()

while True:
    display_temperature_humidity()
    utime.sleep(5)  # Atraso de 5 segundos entre as leituras
