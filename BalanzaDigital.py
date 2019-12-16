# coding=utf-8
from tkinter import *
import serial
import time
import serial.tools.list_ports
from tkinter.ttk import *

def gramosAlibras(valor):
	lib= (float(valor)/453.59237)
	lib2 = ("%.2f" % lib)#extraer 2 sifras significativas
	return lib2

def obeterPuerto():#devuelve el nombre del puerto (string)
	puertos = list(serial.tools.list_ports.comports())
	for port_no, description, address in puertos:#ciclo para variable puertos
		print(port_no)
		print(description)
		print(address)
		print("*****")
		if 'USB' in description:
			return port_no

ArduinoSerial = serial.Serial(obeterPuerto(), 9600, timeout=.1)
time.sleep(2)
ciclo = True
calibrado =False
filtro = 0.25
def promedio():
	estado.set('Obteniendo Datos')
	root.update_idletasks()	
	global ciclo
	ciclo=False
	ArduinoSerial.write(b'p')
	valor=''

	while valor == '':
		valor = (ArduinoSerial.readline().decode('utf-8').strip())# .decode('utf-8').strip())
	ValorGramos.set(valor)
	ValorLibras.set(gramosAlibras(valor))
	estado.set('Promediado')

def lecturaCiclica():
	global ciclo
	if ciclo == True:
		readSerial()
		return
	ciclo = True
	readSerial()

def detenerLectura():
	global ciclo
	ciclo = False
	estado.set('Detenido')
	root.update_idletasks()

def readSerial():
	global estado
	global ciclo
	global filtro
	if ciclo ==True:
		estado.set('Leyendo Sensor')
		root.update_idletasks()		
		ArduinoSerial.write(b'g')
		valor = (ArduinoSerial.readline().decode('utf-8').strip())
		actual=ValorGramos.get()
		#print (valor)
		valorActual = float(actual)
		valorNuevo = float(valor)
		if ((valorNuevo > valorActual+filtro  )or( valorNuevo < valorActual - filtro )):
			ValorGramos.set(valor)
			ValorLibras.set(gramosAlibras(valor))
		else:
			pass
		root.after(500, readSerial)#repetir funcion luego de 500 milis
def calibrar():
	global ciclo
	global estado
	estado.set('Calibrando')
	root.update_idletasks()#actualizar ventana
	ciclo=False
	ArduinoSerial.write(b'c')# escribimos una "C" para llar nuestra funcion calibrar dentro de arduino
	valor = (ArduinoSerial.readline().decode('utf-8').strip())	
	while valor != 'r':
		if estado.get()=='Calibrando':
			estado.set('Calibrando.')
		else:
			estado.set('Calibrando')
		root.update_idletasks()
		time.sleep(.4)	
		valor = (ArduinoSerial.readline().decode('utf-8').strip())
	ArduinoSerial.reset_input_buffer()
	estado.set('listo')
	calibracion.pack_forget()#eliminar el objeto calibracion de nuestra ventana
	readSerial()

root = Tk()#OBJETO DE VENTANA
frameIzquierdo = Frame(root)#objeto de recueadro
frameIzquierdo.pack(side=LEFT,padx = 5)#agregar a la ventana
frameTop =Frame(root)
frameTop.pack(side=TOP)
frameBott = Frame(root)
frameBott.pack(side=BOTTOM)
estado = StringVar()#string para texto del objeto estadoLbl
#estado.set('Iniciado')
ValorGramos=StringVar()#string para texto del objeto de gramos
ValorLibras=StringVar()#string para texto del objeto de libras
ValorGramos.set("0.00")
ValorLibras.set("0.00")
root.title("Balanza")#titulo de la ventana
root.geometry("360x220")#tamaño de la ventana
btn1 = Button(frameIzquierdo, text="Promediar", command=promedio)#boton de promediar
btn2 = Button(frameIzquierdo, text="Leer", command=lecturaCiclica)
btn3 = Button(frameIzquierdo, text="Detener", command=detenerLectura)
btn4 = Button(frameIzquierdo, text="Calibrar", command=calibrar)
estadoLbl = Label(frameIzquierdo, textvariable=estado )
calibracion = Label(frameIzquierdo, text="Sin Calibrar" )
librasLbl=Label(frameTop, text="libras")
libras = Label(frameTop, textvariable=ValorLibras, relief=RAISED,width=6)
libras.config(font=("Courier, 40"))
gramosLbl=Label(frameBott, text="gramos")
gramos = Label(frameBott, textvariable=ValorGramos, relief=RAISED,width=6)
gramos.config(font=("Courier, 40"))
calibracion.pack()
estadoLbl.pack()
btn1.pack(padx = 5, pady = 5)
btn2.pack(padx = 5, pady = 5)
btn3.pack(padx = 5, pady = 5)
btn4.pack(padx = 5, pady = 5)
librasLbl.pack()
libras.pack()
gramosLbl.pack()
gramos.pack( pady = 5)
root.after(500, readSerial())
root.mainloop()