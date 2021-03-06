""" 

Sistema de Control y Monitoreo
     IEH Electricidad 2019

@@@@@@@@@@@@@@ Conexiones @@@@@@@@@@@@@@@@@

@@ Caudalimetro #1 GPIO 17
@@ Caudalimetro #2 GPIO 23
@@ Barometros #1 y #2 conectados al ADS1015
@@ ADS1015  conectado por I2C x48
@@ LCD 2004 conectado por I2C x27

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


"""
#Se importan las Librerias

import Adafruit_ADS1x15
import RPi.GPIO as GPIO
import lcddriver
import time
from time import strftime
import datetime

lcd = lcddriver.lcd()
adc = Adafruit_ADS1x15.ADS1015()
GAIN = 1

#Comando para limpiar la pantalla
#lcd.lcd_clear()

#Mensaje de bienvenida

lcd.lcd_display_string("Monitoreo y Control", 1)
lcd.lcd_display_string("  IEH Electricidad  ", 2)
lcd.lcd_display_string("Fecha: %s" %time.strftime("%d/%m/%Y"),3)
lcd.lcd_display_string("Hora: %s" %time.strftime("%H:%M"),4)
time.sleep(3)
lcd.lcd_clear()

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

contador1 = 0
contador2 = 0

a = 0
b = 0
bsuma = 0
c = 0
d = 0
dsuma = 0
p = 0
t = 0

psuma1 = 0
psuma2 = 0



def my_callback1(channel):
	global contador1
	contador1 = contador1 +1

def my_callback2(channel):
	global contador2
	contador2 = contador2 +1

GPIO.add_event_detect(17, GPIO.FALLING, callback=my_callback1, bouncetime=300)
GPIO.add_event_detect(23, GPIO.FALLING, callback=my_callback2, bouncetime=300)

#Crea el archivo log para el registro
with open("/home/pi/Documents/Programas/Control_Monitoreo/Registro_Sistema.csv","a") as log:

#Loop Principal

	while True:

#Formulas para determinar los caudales
		a = contador1*100
		c = contador2*100
#Se calcula el promedio de 100 muestras
		for p in range(100):
			b = a/30.0
			bsuma = bsuma + b
			d = c/30.0
			dsuma = dsuma + d
		b = bsuma/500.0
		bsuma = 0
		d = dsuma/500.0
		dsuma = 0
#Formulas para determinar las presiones
		valores = [0]*2
		voltajes = [0]*2
		corrientes = [0]*2
		presiones = [0]*2
#Se calcula las presiones promedios de 100 muestras
		for t in range(100):
			for i in range(2):
				valores[i] = adc.read_adc(i, gain=GAIN)
				voltajes[i] = (valores[i]*3.3)/2048
				corrientes[i] = ((voltajes[i]*0.0078)+0.00089)*1000
				presiones[i] = 0.3125*corrientes[i]-1.3
				psuma1 = psuma1 + presiones[0]
				psuma2 = psuma2 + presiones[1]
		presiones[0] = psuma1/500.0
		presiones[1] = psuma2/500.0
		psuma1 = 0
		psuma2 = 0
        	lcd.lcd_display_string("C1 %0.2f[Lt/seg]"%(b) ,1)
		lcd.lcd_display_string("C2 %0.2f[Lt/seg]"%(d),2)
		lcd.lcd_display_string("P1 %0.2f[Bar]"%(presiones[0]),3)
		lcd.lcd_display_string("p2 %0.2f[Bar]"%(presiones[1]),4)
		log.write("{0},{1},{2},{3},{4}\n".format(strftime("%d-%m-%Y %H:%M:%S"),str(b),str(d),str(presiones[0]),str(presiones[1])))
		time.sleep(30)



