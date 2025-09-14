import machine
import time
import uio

pin_sensor = machine.Pin(2, machine.Pin.IN)  # Sensor conectado ao pino 2
factor_conversao = 4.86  # Para converter de frequência para caudal
volume = 0
dt = 0  # Variação de tempo a cada loop
t0 = 0  # millis() do loop anterior

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
    global volume
    global t0
    print("Envie 'r' para reiniciar o volume para 0 Litros")
    uart = machine.UART(0, 9600)  # Configura a UART para comunicação serial

    t0 = time.ticks_ms()  # Obtém o tempo inicial em milissegundos

    while True:
        if uart.any():  # Verifica se há dados disponíveis na UART
            received_char = uart.read(1)  # Lê um caractere da UART
            if received_char == b'r':  # Verifica se é 'r'
                volume = 0  # Redefine o volume se receber 'r'

        frequencia = obter_frequencia()  # Obtém a frequência dos pulsos em Hz
        caudal_L_m = frequencia / factor_conversao  # Calcula o caudal em L/min
        dt = time.ticks_diff(time.ticks_ms(), t0)  # Calcula a variação de tempo em milissegundos
        t0 = time.ticks_ms()  # Atualiza o tempo anterior

        volume += (caudal_L_m / 60) * (dt / 1000)  # volume(L) = caudal(L/min) * tempo(s)

        # Envia pela porta serial
        print("Caudal: {:.3f} L/min\tVolume: {:.3f} L".format(caudal_L_m, volume))
        time.sleep(1)  # Aguarde 1 segundo antes de fazer a próxima leitura

if __name__ == "__main__":
    main()
