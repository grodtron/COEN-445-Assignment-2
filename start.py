# ----- start.py -----

#!/usr/bin/env python

import socket
import sys

host = "localhost"
portA = 6006
portB = 7007
message = "Start"
addrA=(host,portA)
addrB=(host,portB)

print "UDP target IP: ",host
print "UDP target port: ",portA
print "UDP target port: ",portB
print "message: ",message

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.sendto(message,addrA)
sock.sendto(message,addrB)

sock.close()
