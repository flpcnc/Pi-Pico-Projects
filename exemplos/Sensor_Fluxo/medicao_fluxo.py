import machine
import time

pin_sensor = machine.Pin(2, machine.Pin.IN)  # Sensor conectado ao pino 2
factor_conversao = 7.5  # Para converter de frequência para vazão

num_pulsos = 0

def contar_pulsos(pin):
    global num_pulsos
    num_pulsos += 1

# Configurar interrupção no pino 2 (rising edge)
pin_sensor.irq(trigger=machine.Pin.IRQ_RISING, handler=contar_pulsos)

def obter_frequencia():
    global num_pulsos
    num_pulsos = 0
    time.sleep(1)  # Amostra de 1 segundo
    frequencia = num_pulsos  # Hz (pulsos por segundo)
    return frequencia

def main():
    while True:
        frequencia = obter_frequencia()  # Obtem a frequência dos pulsos em Hz
        caudal_L_m = frequencia / factor_conversao  # Calcula o caudal em L/min
        caudal_L_h = caudal_L_m * 60  # Calcula o caudal em L/h

        # Envia pela porta serial
        print("Frequencia de Pulsos: {:.0f} Hz\tCaudal: {:.3f} L/min\tCaudal: {:.3f} L/h".format(frequencia, caudal_L_m, caudal_L_h))
        time.sleep(1)  # Espera um segundo antes de fazer a próxima leitura

if __name__ == "__main__":
    main()
