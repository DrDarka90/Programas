"""Programa para comunicar la Raspby con Ubidots"""

import datetime
import time
from time import strftime
import requests
import random
import Adafruit_ADS1x15
import RPi.GPIO as GPIO
import lcddriver
import requests


#Tokens para el envio de informacion a Ubidots

TOKEN = "BBFF-IH5I4OcjNkdFY6IAcKjnBhbdEThV8j"
DEVICE_LABEL = "Pozo_3_Raspby"
VARIABLE_LABEL_1 = "Presion_1"
VARIABLE_LABEL_2 = "Presion_2"
VARIABLE_LABEL_3 = "Caudal_1"
VARIABLE_LABEL_4 = "Caudal_2"
VARIABLE_LABEL_5 = "Estado"

#Variable de referencia para el LCD 2004

lcd = lcddriver.lcd()

#Variable de referencia para el conversion adc

adc = Adafruit_ADS1x15.ADS1015()
GAIN = 1

#Variables para los caudalimetros

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(4, GPIO.OUT)

contador1 = 0
ISRcontador1 = 0
contador2 = 0
ISRcontador2 = 0
caudal1 = 0
caudal2 = 0
a = 0
b = 0

# Variable de estado del Rele

estado = 0

#Funciones Secuendarias

def my_callback1(channel):
    global ISRcontador1
    ISRcontador1= ISRcontador1 +1

def my_callback2(channel):
    global ISRcontador2
    ISRcontador2 = ISRcontador2 +1

GPIO.add_event_detect(17, GPIO.FALLING, callback=my_callback1, bouncetime=300)
GPIO.add_event_detect(23, GPIO.FALLING, callback=my_callback2, bouncetime=300)
GPIO.output(4, GPIO.LOW)

# Mensaje de Bienvenida al sistema

lcd.lcd_display_string("Monitoreo y Control", 1)
lcd.lcd_display_string("  IEH Electricidad  ", 2)
lcd.lcd_display_string("Fecha: %s" %time.strftime("%d/%m/%Y"),3)
lcd.lcd_display_string("Hora: %s" %time.strftime("%H:%M"),4)
time.sleep(3)
lcd.lcd_clear()

def build_payload(variable_1, variable_2, variable_3, variable_4, variable_5):
    # Crea  el archivo log para el registro de las mediciones
    with open("/home/pi/Documents/Programas/Control_Monitoreo/Registro_Sistema.csv","a") as log:
        global tiempo
        global estado
        tiempo = time.strftime("%H:%M")
	if tiempo == str("18:47"):
            GPIO.output(4, GPIO.HIGH)
	    estado = 1
            lcd.lcd_display_string("ALARMA",1)
            lcd.lcd_display_string("ALARMA",2)
            lcd.lcd_display_string("ALARMA",3)
            lcd.lcd_display_string("ALARMA",4)
            time.sleep(3)
            lcd.lcd_clear()
        # Crea las variables para medir las presiones
        valores = [0]*2
        voltajes = [0]*2
        corrientes = [0]*2
        presiones = [0]*2

        for i in range(2):
            valores[i] = adc.read_adc(i, gain=GAIN)
            voltajes[i] = ((valores[i]*3.3)/2048)*1.37
            corrientes[i] = ((voltajes[i]*0.0064)-0.00016)*1000
            presiones[i] = 0.3125*corrientes[i]-1.3

        # Crea las variables para medir los caudales
        global contador1
        global contador2
        global caudal1
        global caudal2

        if contador1 != ISRcontador1:
            contador1 = ISRcontador1
            a = contador1*100
            caudal1 = a/30.

        if contador2 != ISRcontador2:
            contador2 = ISRcontador2
            b = contador2*100
            caudal2 = b/30.

        # Escribe los datos adquiridos en el archivos de registro
        log.write("{0},{1},{2},{3},{4}\n".format(strftime("%d-%m-%Y %H:%M:%S"),str(caudal1),str(caudal2),str(presiones[0]),str(presiones[1])))

        # Se presentan los datos por pantalla LCD

        lcd.lcd_display_string("C1: %0.2f[Lt/seg]"%(caudal1), 1)
        lcd.lcd_display_string("C2: %0.2f[Lt/seg]"%(caudal2), 2)
        lcd.lcd_display_string("P1: %0.2f[Bar]"%(presiones[0]),3)
        lcd.lcd_display_string("P2: %0.2f[Bar]"%(presiones[1]),4)
        time.sleep(2)
        lcd.lcd_clear()

        # Crea las variables para enviar la informacion
        value_1 = presiones[0]
        value_2 = presiones[1]
        value_3 = caudal1
        value_4 = caudal2
        value_5 = estado

        # Crea el diccionario de carga con la informacion o payload
        payload = {variable_1: value_1,
                   variable_2: value_2,
                   variable_3: value_3,
                   variable_4: value_4,
                   variable_5: value_5}

        return payload

def post_request(payload):
    # Crea los indicadores para la solicitud HTTP
    url = "http://things.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Crea la solicitud por HTTP
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    if status >= 400:
        lcd.lcd_display_string("[INFO] Solicitud ", 1)
        lcd.lcd_display_string("       Rechazada  ", 2)
        lcd.lcd_display_string("Fecha: %s" %time.strftime("%d/%m/%Y"),3)
        lcd.lcd_display_string("Hora: %s" %time.strftime("%H:%M"),4)
        time.sleep(2)
        lcd.lcd_clear()
        print("[ERROR] no se ha podido enviar la data a Ubidots")
        time.sleep(1)
        return False

    print("[INFO] Los datos han sido enviados correctamente")
    lcd.lcd_display_string("[INFO] Solicitud ", 1)
    lcd.lcd_display_string("       Enviada   ", 2)
    lcd.lcd_display_string("Fecha: %s" %time.strftime("%d/%m/%Y"),3)
    lcd.lcd_display_string("Hora: %s" %time.strftime("%H:%M"),4)
    time.sleep(2)
    lcd.lcd_clear()
    return True


def main():
    payload = build_payload(
        VARIABLE_LABEL_1, VARIABLE_LABEL_2, VARIABLE_LABEL_3, VARIABLE_LABEL_4, VARIABLE_LABEL_5)

    print("[INFO] Intentando enviar Datos")
    post_request(payload)
    print("[INFO] Listo!")


if __name__ == '__main__':
    while (True):
        main()
        time.sleep(1)
