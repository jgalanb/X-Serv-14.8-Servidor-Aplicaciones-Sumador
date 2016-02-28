#!/usr/bin/python
# -*- coding: utf-8 -*-

# Jesús Galán Barba
# Ing. en Sistemas de Telecomunicaciones

import socket

class webApp:
	
	def parse(self, request):
		return None

	def process(self, parsedRequest):
		return ("200 OK", "<html><body><h1>It works!</h1></body></html>")

	def extraer_num_peticion(self, request):
		num = int(request.split()[1][1:])
		return num

	def sumador(self, num1, num2):
		sol = num1 + num2
		return sol

	def __init__(self, hostname, port):
		
		mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		mySocket.bind((hostname, port))

		mySocket.listen(1)

		primer_num = None

		try:
			while True:
				print 'Waiting for connections'
				(recvSocket, address) = mySocket.accept()
				print 'HTTP request received (going to parse and process):'
				request = recvSocket.recv(2048)
				print request
				parsedRequest = self.parse(request)
				(returnCode, htmlAnswer) = self.process(parsedRequest)

				try:
					num = self.extraer_num_peticion(request)
				except ValueError:
					recvSocket.send("HTTP/1.1 400 Bad Request\r\n\r\n" +
									"<html><body><h1>ERROR: Hay que introducir numeros! Vuelve a intentarlo...</h1>" +
									"</body></html>" +
									"\r\n")
					recvSocket.close()
					continue

				if (primer_num == None):
						primer_num = num
						print 'Answering back...'
						recvSocket.send("HTTP/1.1 200 OK\r\n\r\n" +
										"<html><body><h1>Me has mandado el numero " + str(primer_num) + "</h1>" +
										"<p><h1>Dame otro numero para poder hacer la suma!</h1></p>" +
										"</body></html>" +
										"\r\n")
				else:
						suma = self.sumador(primer_num, num)
						print 'Answering back...'
						recvSocket.send("HTTP/1.1 200 OK\r\n\r\n" +
										"<html><body><h1>Primero me has mandado el numero " + str(primer_num) + "</h1>" +
										"<p><h1>Luego me has mandado el numero " + str(num) + "</h1></p>" +
										"<p><h1>Y la suma de " + str(primer_num) + " + " + str(num) +
										" es " + str(suma) + "</h1></p>" +
										"</body></html>" +
										"\r\n")
						primer_num = None
		
				recvSocket.close()
				
		except KeyboardInterrupt:
			print "Closing binded socket"
			mySocket.close()
		

if __name__ == "__main__":
    sumador_app = webApp("localhost", 2024)

