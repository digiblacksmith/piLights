# (c) 2014 Aaron Land - Digital Blacksmith

from piLightsColor import *
import copy

class _Programs(object):
	def __init__(self, led_strip, color):
		self.led_strip = led_strip
		self.color = copy.copy(color)
	def run(self, color, vars=0): print 'ERROR'; quit()

## PROGRAMS @@

class Program_All(_Programs):
	def run(self, color, vars=0):
		self.led_strip.fillAll(color)


## TODO: fade out
class Program_ShiftLR(_Programs):
#	def __init__(self, led_strip, color):
#		super(self.__class__, self).__init__(led_strip, color)
#		self.countdown = 0
		
	def run(self, color, var=0):
		limit = var
		if limit > 0:
			self.led_strip.shiftRight(color)
#			self.countdown -= 1
		elif limit < 0:
			self.led_strip.shiftLeft(color)
#			self.countdown += 1
#		else:
#			self.countdown  = limit

## EOF
