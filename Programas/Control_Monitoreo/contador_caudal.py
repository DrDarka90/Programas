"""" Programa para contar la cantidad de pulsos en el Caudalimetro """

# Se importan las Librerias 

import RPi.GPIO as GPIO
import lcddriver
import time 

# Inicio de comunicacion con el LCD 2004
lcd = lcddriver.lcd()

# Comando para limpiar la pantalla
#lcd.lcd_clear()

lcd.lcd_display_string("Monitoreo y Control", 1)
lcd.lcd_display_string("  IEH electricidad  ", 2)
lcd.lcd_display_string(" Sistema OK", 3)
lcd.lcd_display_string(" V1.0 ",4)
time.sleep(4)
lcd.lcd_clear()

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

contador1 = 0
contador2 = 0
a = 0
b = 0
c = 0
d = 0

def my_callback1(channel):
    global contador1
    contador1 = contador1 +1

def my_callback2(channel):
    global contador2
    contador2 = contador2 +1

GPIO.add_event_detect(17, GPIO.FALLING, callback=my_callback1, bouncetime=300)
GPIO.add_event_detect(23, GPIO.FALLING, callback=my_callback2, bouncetime=300)

while True:

	a = contador1*100
	b = a/30
	c = contador2*100
	d = c/30

	lcd.lcd_display_string(" %d "%(contador1), 2)
	lcd.lcd_display_string(" %d "%(contador2), 3)
