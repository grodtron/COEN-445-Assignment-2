from itertools import izip, islice

def from_big_int(data):
	data = hex(data)[2:].replace("L","")
	if len(data) % 2 == 1:
		data = "0" + data
	return ''.join( chr( int(a,16)<<4 | int(b,16) ) for a,b in izip(islice(data, 0, None, 2), islice(data, 1, None, 2)) )
	
def to_big_int(data):
	return reduce( lambda a,b: (a<<8)|ord(b), data, 0 )

out = open("test.txt", "a")
	
class HDLC:

	def __init__(self):
		self.n = 7
		self.k = 3
		self.recv_window_start = 7
		self.recv_window_end   = self.recv_window_start + self.n - 1

		self.send_window_start = 7
		self.send_window_end   = self.send_window_start + self.n - 1
		
		self.flag = 0b01111110
		self.mask = 0b11111
		
	
	def recv(self, data):
		# get approx size in bits
		size = len(data) * 8
		data = to_big_int(data)
		
		out.write(bin(data)+"\n")
		if data & 0xFF != self.flag:
			# TODO send REJ
			return False
		
		# locate true start of message using the flag
		mask   = 0xff << (size - 8)
		target = self.flag << (size - 8)
		while mask & data != target:
			mask   = mask >> 1
			target = target >> 1
			size -= 1
		# clear flags
		data ^= target
		data = data >> 8
		size -= 16
		
		data, size = self._unbitstuff(data, size)
		out.write(bin(data)+"\n")
		
		address = data >> (size-8)
		control = (data >> (size-16)) & 0xFF
		data    = ((((1 << (size-16))-1)&data) >> 16)

		out.writelines((bin(address), bin(control), bin(data)))
		# prepend control
		# prepend address
		# append FCS (dummy)
		# bit stuffing
		# append / prepend flags
		# send
		pass
	
	def send(self, address, data, size):
		data = (((address<<(size+8)) | (self._makecontrol()<<size) | data)<<16) | 0x0F55
		size += 32
		data, size = self._bitstuff(data, size)
		data = (((0b01111110<<size) | data)<<8) | 0b01111110
		return data
	
	def _makecontrol(self):
		control = (self.send_window_start<<4) | self.recv_window_start
		self.send_window_start += 1
		return control
	
	def _bitstuff(self, data, size):
		width = size
		i = width
		m = self.mask << i
		while m != self.mask:
			if m & data == m:
				# mask off all the bits below the current position of the five sequential 1s
				tmp_mask  = (1 << i) - 1
				# extend the mask to the right length
				tmp_mask |= 1 << width
				# invert the mask so that it masks the 5 1s and everything above.
				# have to use weird xor shit, since regular ~ doesn't work properly
				tmp_mask ^= (1 << (width + 1)) - 1
				# Shift the top half up and OR with the bottom half to insert a 0.
				data = ((data & tmp_mask) << 1) | (data & ~tmp_mask)
				
				width += 1
				# could optimize by incrementing i conditionally, but I don't care enough
			m = m >> 1
			i -= 1
		return data, width

	def _unbitstuff(self, data, length):
		width = length + 1
		i = 0
		m = self.mask << 1
		m2 = 1
		while i < width:
			if (m & data == m) and (m2 & data == 0):
				# mask off all the bits below the current position of the five sequential 1s
				# followed by a zero
				tmp_mask  = (1 << i) - 1
				# extend the mask to the right length
				tmp_mask |= 1 << width
				# invert the mask so that it masks the 5 1s and zero and everything above.
				# have to use weird xor shit, since regular ~ doesn't work properly
				tmp_mask ^= (1 << (width + 1)) - 1
				# Shift the top half down and OR with the bottom half to insert a 0.
				data = ((data & tmp_mask) >> 1) | (data & ~tmp_mask)

				width -= 1
				# could optimize by incrementing i conditionally, but I don't care enough
			m  = m << 1
			m2 = m2 << 1
			i += 1
		return data, width-1
				

if __name__ == '__main__':
	hdlc = HDLC()
	
	data = hdlc.send(1, 0b10101, 5)
	out.write(bin(data)+"\n")
	data = from_big_int(data)
	out.write(repr(data)+"\n")
	hdlc.recv(data)
