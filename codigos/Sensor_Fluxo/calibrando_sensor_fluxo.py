import machine
import time

pin_sensor = machine.Pin(2, machine.Pin.IN)  # Sensor conectado ao pino 2
num_pulsos = 0

def contar_pulsos(pin):
    global num_pulsos
    num_pulsos += 1

# Configurar interrupção no pino 2 (rising edge)
pin_sensor.irq(trigger=machine.Pin.IRQ_RISING, handler=contar_pulsos)

def calibrar_sensor():
    global num_pulsos
    num_pulsos = 0
    volume = float(input("Digite o volume (em litros) medido pelo sensor: "))
    print("Despejar o liquido no sensor conforme valor em Litros informado acima...")
    time.sleep(60)  # Aguarde 60 segundos para medir o número de pulsos

    k = num_pulsos / (volume * 60)  # Calcula o fator de conversão
    return k

def main():
    print("Calibrando o sensor de fluxo...")
    fator_conversao = calibrar_sensor()
    print("Fator de Conversao calculado:", fator_conversao)
    print("Aguarde...")
    

    while True:
        # Envia pela porta serial
        print("Numero de Pulsos =", num_pulsos)
        time.sleep(1)  # Aguarde 1 segundo antes de fazer a próxima leitura

if __name__ == "__main__":
    main()
