# ----- sendA.py ------

#!/usr/bin/env python

import socket
import sys
from time import sleep

def sendA(message):
	host ="localhost"
	portA = 6006
	addrA = (host,portA)

	sleep(0.5)
	sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	sock.sendto(message,addrA)

	return 1
