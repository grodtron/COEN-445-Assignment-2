# ----- sendB.py ------

#!/usr/bin/env python

import socket
import sys
from time import sleep

def sendB(message):
	host ="localhost"
	portB = 7007
	addrB = (host,portB)

	sleep(0.5)
	sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	sock.sendto(message,addrB)

	return 1
