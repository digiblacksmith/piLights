# (c) 2014 Aaron Land - Digital Blacksmith

from piLightsColor import *

class _Patterns(object):
	def __init__(self, buffer, on=False):
		self.buffer = buffer
		self.ON = on
	def run(self, color): print 'ERROR _Patterns.run()'; quit()

## PROGRAMS @@

class Pattern_All(_Patterns):
	def run(self, color):
		self.buffer.fillAll(color)


## TODO: fade out
class Pattern_BitShift(_Patterns):
	def __init__(self, buffer, direction=1):
		super(self.__class__, self).__init__(buffer)
		self.direction = direction
	
	def run(self, color):
		if self.direction > 0:
			for x in range(self.direction):
				self.buffer.shiftRight(color)
		elif self.direction < 0:
			for x in range(self.direction):
				self.buffer.shiftLeft(color)

## EOF
