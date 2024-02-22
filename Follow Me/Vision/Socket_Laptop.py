#librerias
import socket

#Inicio Socket
IP_RASP = "192.168.43.91" #IP de la Rasp
PUERTO = 5000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP_RASP, PUERTO))
#funciones
def Socket(datos):
	data=str(datos)
	sock.sendall(data.encode())

#Execution
while True:
	break
sock.close()
