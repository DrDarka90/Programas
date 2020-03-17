#Codigo para el testeo de los servomotores de la torreta

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) #Desactiva las  advertencias del GPIO
GPIO.setup(4, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)


b = GPIO.PWM(4, 50) # servo horizontal
p = GPIO.PWM(17, 50) # servo vertical

b.start(2.5)  # posicion inicial en Duty Cycle  del servo horizontal
p.start(10.0) # posicion incial en Duty Cycle  del servo vertical

try:
    while True:
#Esta es una rutina de movimientos basica de la torreta

#El for permite a la torreta moverse horizontalmente de 0 a 180 grados

#Siendo 0 = 2.5 y 180 = 12.5, debido a que el for no puede tener float se tiene que multiplicar por 10 para poder trabajarlo como int, luego se divide
        
        for a in range (int(2.5*10),int(12.5*10),int(0.5*10)): #movimiento de izquierda a derecha
            realA = a/10.0
            b.ChangeDutyCycle(realA)
            time.sleep(0.5)
            p.ChangeDutyCycle(8) #movimiento de la plataforma hacia arriba
            time.sleep(1)
            p.ChangeDutyCycle(12.5) #movimiento de la plataforma hacia abajo
            time.sleep(1)

        for c in range (int(12.5*10),int(2.5*10),-int(0.5*10)): #movimiento de derecha a izquierda
            realC = c/10.0
            b.ChangeDutyCycle(realC)
            time.sleep(0.5)
            p.ChangeDutyCycle(8)
            time.sleep(1)
            p.ChangeDutyCycle(12.5)
            time.sleep(1)

except KeyboardInterrupt:
    b.stop()
    p.stop()
    GPIO.cleanup()

