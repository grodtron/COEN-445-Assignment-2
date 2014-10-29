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
		# prepend control
		# prepend address
		# append FCS (dummy)
		# bit stuffing
		# append / prepend flags
		# send
		pass
	
	def send(self, data):
		# prepend control
		# prepend address
		# append FCS (dummy)
		# bit stuffing
		# append / prepend flags
		# send
		pass
	
	def _stuff(self, data):
		width = (10**5)
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
		return data

	def _unstuff(self, data, length):
		width = length
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
				#print "  " + bin(data)
				#print "  " + bin(tmp_mask & 0b1111111111111111111111111111111111111111111111111111111111)
				# Shift the top half down and OR with the bottom half to insert a 0.
				data = ((data & tmp_mask) >> 1) | (data & ~tmp_mask)

				width -= 1
				# could optimize by incrementing i conditionally, but I don't care enough
			m  = m << 1
			m2 = m2 << 1
			i += 1
			#print("   -")
		return data
				

if __name__ == '__main__':
	# msg = randint(0, 1<<(10**5))
	hdlc = HDLC()
	
	for i in xrange(2**30):
		if i != hdlc._unstuff(hdlc._stuff(i), len(bin(i))-2):
			print "Error on " + str(i)
			print "  original => " + bin(i)
			print "  stuff    => " + bin(hdlc._stuff(i))
			print "  unstuff  => " + bin(hdlc._unstuff(hdlc._stuff(i), len(bin(i))-2))
			
