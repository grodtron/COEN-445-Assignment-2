# ----- listenB.py ------

#!/usr/bin/env python

import socket
import sys

host ="localhost"
portB = 7007
addrB = (host,portB)
timeout = 10

def openB():

	global sockB
	sockB=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	sockB.bind(addrB)

def listenB():
	sockB.settimeout(timeout)
	data,address = sockB.recvfrom(1024)
	print data
	if (data == "&DISCONNECT&"):
		sockB.close()
	return data
