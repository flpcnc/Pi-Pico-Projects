# =============================================================================
# ESTAÇÃO AMBIENTAL - RASPBERRY PI PICO + MICROPYTHON
# =============================================================================
# Projeto: Monitor de condições ambientais com DHT11, BMP280 e Display OLED
# Autor: FLPCNC
# =============================================================================

from machine import Pin, I2C
import utime
import math
from config import *

# Importações condicionais baseadas na configuração
if USE_OLED:
    import ssd1306

if USE_DHT11:
    import dht

if USE_BMP280:
    from bmp280 import *

# =============================================================================
# INICIALIZAÇÃO DO HARDWARE
# =============================================================================

def init_hardware():
    """Inicializa os componentes de hardware baseado na configuração"""
    components = {}
    
    # Inicializar OLED
    if USE_OLED:
        try:
            i2c_oled = I2C(1, sda=Pin(OLED_SDA_PIN), scl=Pin(OLED_SCL_PIN), freq=OLED_I2C_FREQ)
            components['oled'] = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c_oled)
            print("✓ OLED inicializado")
        except Exception as e:
            print(f"✗ Erro ao inicializar OLED: {e}")
            components['oled'] = None
    
    # Inicializar DHT11
    if USE_DHT11:
        try:
            components['dht11'] = dht.DHT11(Pin(DHT11_PIN))
            print("✓ DHT11 inicializado")
        except Exception as e:
            print(f"✗ Erro ao inicializar DHT11: {e}")
            components['dht11'] = None
    
    # Inicializar BMP280
    if USE_BMP280:
        try:
            i2c_bmp = I2C(0, sda=Pin(BMP280_SDA_PIN), scl=Pin(BMP280_SCL_PIN), freq=BMP280_I2C_FREQ)
            components['bmp280'] = BMP280(i2c_bmp)
            
            # Configurar caso de uso
            if BMP280_USE_CASE == "INDOOR":
                components['bmp280'].use_case(BMP280_CASE_INDOOR)
            elif BMP280_USE_CASE == "HANDHELD":
                components['bmp280'].use_case(BMP280_CASE_HANDHELD_DYN)
            elif BMP280_USE_CASE == "WEATHER":
                components['bmp280'].use_case(BMP280_CASE_WEATHER)
            
            print("✓ BMP280 inicializado")
        except Exception as e:
            print(f"✗ Erro ao inicializar BMP280: {e}")
            components['bmp280'] = None
    
    return components

# =============================================================================
# FUNÇÕES DE LEITURA DOS SENSORES
# =============================================================================

def read_dht11(dht_sensor):
    """Lê dados do sensor DHT11"""
    if not dht_sensor:
        return None, None
    
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        
        # Verifica se as leituras são válidas
        if isinstance(temperature, (int, float)) and isinstance(humidity, (int, float)):
            return int(temperature), int(humidity)
        else:
            return None, None
    except Exception as e:
        print(f"Erro ao ler DHT11: {e}")
        return None, None

def read_bmp280(bmp_sensor):
    """Lê dados do sensor BMP280 e calcula altitude"""
    if not bmp_sensor:
        return None, None, None
    
    try:
        pressure = bmp_sensor.pressure
        temperature = bmp_sensor.temperature
        
        # Converter pressão para mmHg
        p_mmHg = round(pressure / 133.322, PRESSURE_DECIMAL_PLACES)
        
        # Calcular pressão ao nível do mar baseada na altitude local
        sea_level_pressure = pressure / math.pow(1 - ALTITUDE_LOCAL / 44330.0, 5.255)
        
        # Calcular altitude baseada na pressão ao nível do mar
        altitude = int(44330.0 * (1 - math.pow(sea_level_pressure / 101325.0, 1/5.255)))
        
        return int(temperature), altitude, p_mmHg
    except Exception as e:
        print(f"Erro ao ler BMP280: {e}")
        return None, None, None

# =============================================================================
# FUNÇÕES DE SAÍDA
# =============================================================================

def display_on_oled(oled, data):
    """Exibe dados no display OLED"""
    if not oled or not USE_OLED:
        return
    
    try:
        oled.fill(0)
        oled.text(f"   {PROJECT_NAME}   ", 0, 0)
        
        # Linha 1: Temperaturas
        temp_line = ""
        if data['temp_dht11'] is not None:
            temp_line += f"T1 {data['temp_dht11']}C "
        if data['temp_bmp280'] is not None:
            temp_line += f"T2 {data['temp_bmp280']}C"
        oled.text(temp_line, 0, 16)
        
        # Linha 2: Umidade e Altitude
        env_line = ""
        if data['humidity'] is not None:
            env_line += f"UR: {data['humidity']}% "
        if data['altitude'] is not None:
            env_line += f"Alt: {data['altitude']}"
        oled.text(env_line, 0, 32)
        
        # Linha 3: Pressão
        if data['pressure_mmHg'] is not None:
            oled.text(f"mmHg: {data['pressure_mmHg']:.{PRESSURE_DECIMAL_PLACES}f}", 0, 48)
        
        oled.show()
    except Exception as e:
        print(f"Erro ao exibir no OLED: {e}")

def log_to_csv(data):
    """Salva dados no arquivo CSV"""
    if not USE_CSV_LOG:
        return
    
    try:
        # Criar cabeçalho se arquivo não existir
        try:
            with open(CSV_FILENAME, "r") as f:
                pass  # Arquivo existe
        except OSError:
            # Arquivo não existe, criar com cabeçalho
            with open(CSV_FILENAME, "w") as f:
                f.write(CSV_HEADER + "\n")
        
        # Adicionar dados
        timestamp = utime.localtime()
        csv_line = f"{timestamp},{data['temp_dht11']},{data['humidity']},{data['temp_bmp280']},{data['altitude']},{data['pressure_mmHg']:.{PRESSURE_DECIMAL_PLACES}f}"
        
        with open(CSV_FILENAME, "a") as f:
            f.write(csv_line + "\n")
            
    except Exception as e:
        print(f"Erro ao salvar CSV: {e}")

def print_to_console(data):
    """Imprime dados no console"""
    if not USE_CONSOLE:
        return
    
    output_parts = []
    
    if data['temp_dht11'] is not None:
        output_parts.append(f"Temp DHT11: {data['temp_dht11']}°C")
    
    if data['humidity'] is not None:
        output_parts.append(f"Umidade: {data['humidity']}%")
    
    if data['temp_bmp280'] is not None:
        output_parts.append(f"Temp BMP280: {data['temp_bmp280']}°C")
    
    if data['altitude'] is not None:
        output_parts.append(f"Altitude: {data['altitude']}m")
    
    if data['pressure_mmHg'] is not None:
        output_parts.append(f"Pressão: {data['pressure_mmHg']:.{PRESSURE_DECIMAL_PLACES}f} mmHg")
    
    if output_parts:
        print(" | ".join(output_parts))

# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================

def main():
    """Função principal do programa"""
    print("=" * 50)
    print(f"🌡️  ESTAÇÃO AMBIENTAL - {PROJECT_NAME}")
    print("=" * 50)
    print(f"DHT11: {'✓' if USE_DHT11 else '✗'}")
    print(f"BMP280: {'✓' if USE_BMP280 else '✗'}")
    print(f"OLED: {'✓' if USE_OLED else '✗'}")
    print(f"CSV Log: {'✓' if USE_CSV_LOG else '✗'}")
    print(f"Intervalo: {READING_INTERVAL}s")
    print("=" * 50)
    
    # Inicializar hardware
    components = init_hardware()
    
    print("🚀 Iniciando monitoramento...")
    print("-" * 50)
    
    # Loop principal
    while True:
        try:
            # Estrutura de dados
            data = {
                'temp_dht11': None,
                'humidity': None,
                'temp_bmp280': None,
                'altitude': None,
                'pressure_mmHg': None
            }
            
            # Ler sensores
            if USE_DHT11 and components.get('dht11'):
                data['temp_dht11'], data['humidity'] = read_dht11(components['dht11'])
            
            if USE_BMP280 and components.get('bmp280'):
                data['temp_bmp280'], data['altitude'], data['pressure_mmHg'] = read_bmp280(components['bmp280'])
            
            # Saídas
            display_on_oled(components.get('oled'), data)
            log_to_csv(data)
            print_to_console(data)
            
            # Aguardar próxima leitura
            utime.sleep(READING_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n🛑 Monitoramento interrompido pelo usuário")
            break
        except Exception as e:
            print(f"❌ Erro no loop principal: {e}")
            utime.sleep(5)  # Aguardar antes de tentar novamente

# =============================================================================
# EXECUÇÃO
# =============================================================================

if __name__ == "__main__":
    main()