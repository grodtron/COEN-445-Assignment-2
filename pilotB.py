# ----- pilotB.py ------

#!/usr/bin/env python

from listenB import *
from sendA import *

openB()

sendA("No, can't hear you")

sendA("... or can I...?")

listenB()

sendA("Okay signing out")

sendA("&DISCONNECT&")

listenB()

listenB()
