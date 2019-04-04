import RPi.GPIO as GPIO
import os

contaA = 0
contaB = 0

#Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN)
GPIO.setup(24,GPIO.IN)

#Callbacks
def CuentaA(channel):
    global contaA
    contaA += 1
    os.system("clear")
    print "Contador A: ", contaA
    print "Contador B: ", contaB

def CuentaB(channel):
    global contaB
    contaB += 1
    os.system("clear")
    print "Contador A: ", contaA
    print "Contador B: ", contaB

#Interrupciones
GPIO.add_event_detect(23, GPIO.RISING, callback = CuentaA)
GPIO.add_event_detect(24, GPIO.RISING, callback = CuentaB)

print "Contador A: ", contaA
print "Contador B: ", contaB

#Bucle principal
while(1):
    pass

GPIO.cleanup()
