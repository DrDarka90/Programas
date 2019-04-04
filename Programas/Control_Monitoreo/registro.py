"""Programa que permite registrar datos en la raspberry"""

#Se importa las librerias necesarias 
import time
import datetime

#Ruta del Archivo
log_path = "/var/log/iot/"

#Escribe un archivo log_path con el nombre  en el formato dd-mm-yyyy.log

def write_log(text):
	log = open(log_path + datetime.datetime.now().strftime("%d-%m-%Y") + "_dht.log","a")
	line = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " " + text + "\n"
	log.write(line)
	log.close()

#En esta seccion se agrega la lectura de los sensores y escritura en el archivo log

#Intenta ejectuar las instrucciones, si falla va a la instruccion except
try:
	#Loop Principal
	while True:
		#desde aqui se hace lectura de los sensores y se escribe
		write_log("Hola mundo")
	time.sleep(10)

#Se ejecuta en caso de que falle alguna instruccion dentro del try
except Exception,e:
	#Registra el error en el archivo log y termina la ejecucion
	write_log(str(e))
