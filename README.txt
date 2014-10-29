*** USAGE ***

Call function "openX()" for a station X to open/setup its hardcoded socket
Call function "listenX()" for a station X to listen to check its buffer for any data
  To avoid hanging, a timeout of 10 secs is hardcoded
Refer to pilot scripts

*** NOTES ***

Addresses are hardcoded for now.
Both stations talk through localhost, portA = 6006 and portB = 7007
Something wonky happens 2 stations are out of sync.
  Solution 1: have a server spawn a client thread (unrealistic)
  Solution 2: server's socket should stay open indefinately (no timeout) and wait until client initiates,
              then sets timeout for future interactions until client gives up
