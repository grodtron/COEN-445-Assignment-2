from itertools import izip, islice

def from_big_int(data, length):
	data = hex(data)[2:-1].zfill(length)
	return ''.join( chr( int(a,16)<<4 | int(b,16) ) for a,b in izip(islice(data, 0, None, 2), islice(data, 1, None, 2)) )
	
def to_big_int(data):
	return reduce( lambda a,b: (a<<8)|ord(b), data, 0 )


class HDLC:

	def __init__(self):
		self.n = 7
		self.k = 3
		self.recv_window_start = 0
		self.recv_window_end   = self.recv_window_start + self.n - 1

		self.send_window_start = 0
		self.send_window_end   = self.send_window_start + self.n - 1
		
		self.flag = 0b01111110
		self.mask = 0b11111
		
	
	def recv(self):
		data = b'thisissomeshitrighthere'
		size = 1
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
		pass
	
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
		return data
				

if __name__ == '__main__':
	hdlc = HDLC()
	
	print repr(from_big_int(0x00010203040506070809, 20))
	print hex(to_big_int(from_big_int(0x00010203040506070809, 20)))
			
