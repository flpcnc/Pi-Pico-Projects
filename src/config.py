# =============================================================================
# CONFIGURAÇÕES DA ESTAÇÃO AMBIENTAL - RASPBERRY PI PICO
# =============================================================================

# --------------------------------------------------------------------------
# SENSORES HABILITADOS (True/False)
# --------------------------------------------------------------------------
USE_DHT11 = True        # Sensor de temperatura e umidade DHT11
USE_BMP280 = True       # Sensor de pressão e temperatura BMP280
USE_FLOWMETER = False   # Sensor de fluxo YF-S201 (ainda não implementado)

# --------------------------------------------------------------------------
# SAÍDAS HABILITADAS (True/False)
# --------------------------------------------------------------------------
USE_OLED = True         # Display OLED para mostrar dados
USE_CSV_LOG = True      # Salvar dados em arquivo CSV
USE_CONSOLE = True      # Imprimir dados no console/serial

# --------------------------------------------------------------------------
# CONFIGURAÇÕES DE TIMING
# --------------------------------------------------------------------------
READING_INTERVAL = 15   # Intervalo entre leituras (em segundos)

# --------------------------------------------------------------------------
# CONFIGURAÇÕES DE HARDWARE - PINAGEM
# --------------------------------------------------------------------------
# DHT11
DHT11_PIN = 22

# BMP280 (I2C)
BMP280_SDA_PIN = 0
BMP280_SCL_PIN = 1
BMP280_I2C_FREQ = 20000

# OLED (I2C)
OLED_SDA_PIN = 2
OLED_SCL_PIN = 3
OLED_I2C_FREQ = 40000
OLED_WIDTH = 128
OLED_HEIGHT = 64

# YF-S201 (para implementação futura)
FLOWMETER_PIN = 2

# --------------------------------------------------------------------------
# CONFIGURAÇÕES ESPECÍFICAS
# --------------------------------------------------------------------------
# Localização para cálculo de altitude (pressão ao nível do mar)
ALTITUDE_LOCAL = 689.0  # Altitude média de São Carlos, SP (em metros)

# Nome do projeto (exibido no OLED)
PROJECT_NAME = "FLPCNC"

# Nome do arquivo CSV
CSV_FILENAME = "data.csv"

# Cabeçalho do CSV (criado automaticamente se não existir)
CSV_HEADER = "timestamp,temp_dht11,humidity_dht11,temp_bmp280,altitude,pressure_mmHg"

# --------------------------------------------------------------------------
# CONFIGURAÇÕES AVANÇADAS
# --------------------------------------------------------------------------
# Caso de uso do BMP280 (ver biblioteca bmp280.py)
BMP280_USE_CASE = "INDOOR"  # Opções: INDOOR, HANDHELD, WEATHER, etc.

# Precisão de casas decimais para pressão
PRESSURE_DECIMAL_PLACES = 2