import pyb
import dht
SSID='WIFI-ITM'                 # Nombre de la conexion wifi
PSW =''													# Clave para entrar a la RED.
esp01=pyb.UART(1,115200)
#IP_Thingspeak='184.106.153.149'
IP_Thingspeak='api.thingspeak.com'
port='80'
d = dht.DHT11(Pin('X1'))
def cmd_RST():
	# Resetea el modulo ESP-01 or ESP8266
	# AT
	esp01.write('AT+RST\r\n')
	pyb.delay(300)
	r=esp01.read()

def cmd_AT():
	# Prueba a ver si esta bien conectada la ESP
	# AT
	esp01.write('AT\r\n')
	pyb.delay(300)
	r=esp01.read()
	esp01.write('AT\r\n')
	pyb.delay(1000)
	r=esp01.read()
	print("%s"%r)
	pyb.delay(500)
	if (r[7:9]==b'OK'):
		print("Correcto, Responde!!")
	else:
		print("falso, resetee la ESP")
	pyb.delay(500)
	r=esp01.read()


def cmd_CWMODE():
	# Empieza la configuracion del modo de operacion de la ESP
	# CWMODE = 1  Cofigura la ESP en modo ST (Station) 
	# CWMODE = 2  Cofigura la ESP en modo AP (Acces Point)
	# CWMODE = 3  Cofigura la ESP en modo ST+AP
	esp01.write('AT+CWMODE=3\r\n')
	pyb.delay(1000)
	r=esp01.read()
	print("%s"%r)
	pyb.delay(500)
	if (r[16:18]==b'OK'):
		print("Correcto, AT+CWMODE=1")
	else:
		print("falso, no configuro CWMODE")
	pyb.delay(500)
	r=esp01.read()

def cmd_CWJAP(ssid,psw):
	# Conecta la ESP a una red WIFI teniendo un SSID (nombre de la red) y PSW (contraseña de la red) conocidos
	# tanto SSID como PSW deben mandarse como cadenas dentro de "SSID"
	esp01.write('AT+CWJAP=' + '\"' + ssid + '\",\"' + psw + '\"\r\n')
	pyb.delay(100)
	r=esp01.read()
	print("%s"%r)
	pyb.delay(3000)
	r=esp01.read()
	print("%s"%r)
	pyb.delay(500)
	if r[5:14]==b'CONNECTED':
		print("%s"%r)
		print("ESP Conectada a internet!!!")
	else:
		print("falso, no configuro CWMODE")
	pyb.delay(6000)
	r=esp01.read()
	
def cmd_CIFSR():
	# Prengunta la direcion IP que le fue asignada a la ESP-01 dentro de la red por ejemplo "IP=102.167.0.1"
	# Tambien entrega el valor de la MAC de la ESP-01 normalmente la MAC completa pero tambien puede entregar la SMAC que es la MAC abreviada
	esp01.write('AT+CIFSR\r\n')
	pyb.delay(100)
	r=esp01.read()
	rr=str(r)
	
	IP=rr[rr.find('IP')+4:rr.find("+CIFSR:STAMAC")-5]
	MAC=rr[rr.find("MAC")+5:len(rr)-1]
	print("%s"%r)
	print("la IP es %s"%IP)
	print("la mac es %s"%MAC)
	pyb.delay(500)
	r=esp01.read()
	
def cmd_CIPMODE():
	# Set transfer mode
	# 0 unvarnished conection mode = modo de conexion transparente (when use send you need +IPD,strlen()) max 2048 carateres a enviar por envio
	# 1 modo de conexion normal (when use send you need only strlen()) max 2048 carateres a enviar por envio
	esp01.write('AT+CIPMODE=0\r\n')
	pyb.delay(100)
	r=esp01.read()
	print("%s"%r)
	pyb.delay(100)
	r=esp01.read()

def cmd_CIPMUX():
	# Habilita conecxiones multiples o no 
	# 0 Single connection
    # 1 Multiple connections (MAX 4)
	esp01.write('AT+CIPMUX=0\r\n')
	pyb.delay(100)
	r=esp01.read()
	print("%s"%r)
	pyb.delay(100)
	r=esp01.read()

def cmd_CIPSTART():
	# Establish TCP connection or register UDP port and start a connection
	# Set	AT+CIPSTART=type,addr,port (Single connection mode)
	# Set   AT+CIPSTART=id,type,addr,por (Multiple connection mode)
	# id: 0-4, id of connection
	# type: String, “TCP” or “UDP”
	# addr: String, remote IP
	# port: String, remote port
	esp01.write('AT+CIPSTART=\"TCP\",\"' + IP_Thingspeak + '\",' + port + '\r\n')
	pyb.delay(100)
	r=esp01.read()
	print("%s"%r)
	pyb.delay(100)
	r=esp01.read()	

	"""" 
		to configure the data length in normal transmission mode.
		1. Single connection: (+CIPMUX=0)
		AT+CIPSEND=<length>
		2. Multiple connections: (+CIPMUX=1)
		AT+CIPSEND=<link	ID>,<length>
		3. Remote IP and ports can be set in UDP
		transmission:
		AT+CIPSEND=[<link	ID>,]<length>	[,<remote	
		IP>,<remote	port>] 
		
		 to start sending data in transparent transmission mode
		 AT+CIPSEND
		 
		 <link	ID>: ID of the connection (0~4), for multiple connections.
		• <length>: data length, MAX: 2048 bytes.
		• [<remote	IP>]: remote IP can be set in UDP transmission.
		• [<remote	port>]: remote port can be set in UDP transmission.
		"""	

def cmd_CIPSENDEX():
	# 1. Single connection: (+CIPMUX=0)
	#    AT+CIPSENDEX=<length>
	# 2. Multiple connections: (+CIPMUX=1)
	#    AT+CIPSENDEX=<link	ID>,<length>
	# 3. Remote IP and ports can be set in UDP transmission:
	#    AT+CIPSENDEX=[<link	ID>,]<length>[,<remote	IP>,<remote	port>]
	# PARAMETERS
	# • <link	ID>: ID of the connection (0~4), for multiple connections.
	# • <length>: data length, MAX: 2048 bytes.
	# • When the requirement of data length, determined by <length>, is met, or when \0 appears, the transmission of data starts. Go back to the normal command mode and wait for the next AT command.
	# • When sending \0, please send it as \\0.
	# <length> en python la longitud de una cadena es ----> len(string)   D5GTE3AEB0UO1ENN
	d.measure()
	dT=d.temperature() # eg. 23 (°C)
	dH=d.humidity()    # eg. 41 (% RH)# XXXTE3AEB0UO1XXX esta Api key le faltan 6 digitos this API key dont have six digits XXX__XXX
	url="GET /update?api_key=XXXTE3AEB0UO1XXX&field1="+str(dT)+"&field2="+str(dH)+"&headers=false HTTP/1.1\r\n" + "Host: " + IP_Thingspeak + "\r\n" + "Connection: close\r\nAccept: */*\r\n\r\n"
	print("\r\n")
	esp01.write('AT+CIPSEND='+str(len(url))+'\r\n')
	pyb.delay(1000)
	r=esp01.read()
	rr=str(r)
	print("\r\n")
	n=rr.find('>')
	pyb.delay(2000)
	#print("%s"%rr[n])
	print(">%s"%url)
	print("\r\n")
	esp01.write(url)
	pyb.delay(100)
	r=esp01.read()
	pyb.delay(100)
	print("%s"%r)
	pyb.delay(100)
	r=esp01.read()
	
def cmd_CIPCLOSE():
	# Set	AT+CIPCLOSE=id	response = OK	Close TCP or UDP connection For multiply connection mode
	# Set	AT+CIPCLOSE	    response = OK	Close TCP or UDP connection For single connection mode
	esp01.write('AT+CIPCLOSE \r\n')
	pyb.delay(100)
	r=esp01.read()
	print("%s"%r)
	
cmd_RST()
cmd_AT()
cmd_CWMODE()
cmd_CWJAP(SSID,PSW)
#cmd_CIFSR()
cmd_CIPMODE()
cmd_CIPMUX()
while True:
	cmd_CIPSTART()
	pyb.delay(3000)
	cmd_CIPSENDEX()
	pyb.delay(15000)
	#cmd_CIPCLOSE()
	#pyb.delay(1000)
