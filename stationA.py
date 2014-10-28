# ----- stationA.py ------

#!/usr/bin/env python

import socket
import sys
from time import sleep

host ="localhost"
portA = 6006
portB = 7007
addrA = (host,portA)
addrB = (host,portB)


sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(addrA)

#Waiting for start signal
while True:
	data,address = sock.recvfrom(1024)
	if data=="Start":
		break

while True:
	sleep(0.5)
	message = "Hi B, this is A"
	sock.sendto(message,addrB)

	data,address = sock.recvfrom(1024)
	print str(data)

sock.close()
