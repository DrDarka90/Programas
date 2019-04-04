""" Codigo para la lectura de los barometros y presentacion por LCD 2004"""

import Adafruit_ADS1x15
import lcddriver
import time

#Inicio de la comunicacion con el LCD 2004
lcd = lcddriver.lcd()
#Inicio de la comunicacion con el conversor ADS1015
adc = Adafruit_ADS1x15.ADS1015()
GAIN = 1

# Mensaje de bienvenida

lcd.lcd_display_string("Sistema de medicion",1)
lcd.lcd_display_string(" IEH Electricidad",2)
lcd.lcd_display_string(" Sistema OK ",3)
lcd.lcd_display_string("Fecha: %s" %time.strftime("%d/%m/%Y"),4)
time.sleep(2)
lcd.lcd_clear()

#Main loop
while True:
	valores = [0]*2
	voltajes = [0]*2
	corrientes = [0]*2
	presiones = [0]*2

	for i in range(2):
		valores[i] = adc.read_adc(i, gain=GAIN)
		voltajes[i] = (valores[i]*3.3)/2048
		corrientes[i] = ((voltajes[i]*0.0078)+0.00089)*1000
		presiones[i] = 0.3125*corrientes[i]-1.3

	lcd.lcd_display_string("Barometro No.1" ,1)
	lcd.lcd_display_string(" %.2f "%(corrientes[0]),2)
	lcd.lcd_display_string("Barometro No.2" ,3)
	lcd.lcd_display_string(" %.2f "%(corrientes[1]),4)
	time.sleep(0.5)
