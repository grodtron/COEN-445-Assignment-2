# ----- listenA.py ------

#!/usr/bin/env python

import socket
import sys

host ="localhost"
portA = 6006
addrA = (host,portA)
timeout = 10

def openA():

	global sockA
	sockA=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	sockA.bind(addrA)

def listenA():
	sockA.settimeout(timeout)
	data,address = sockA.recvfrom(1024)
	print data
	if (data == "&DISCONNECT&"):
		sockA.close()
	return data
