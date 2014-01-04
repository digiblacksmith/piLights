# (c) 2014 Aaron Land - Digital Blacksmith

from piLightsColor import *
import copy, types, math, random

class _Channels(object):
	def tick(self, color, channels, vars=0): print 'ERROR'; quit()

## CHANNELS @@

class Channel_Blink(_Channels):
	def __init__(self):
		self.off = True
		self.period = 0
	def tick(self, color, channels, vars=0):
		self.period += 1
		if self.period >= vars[0]:
			self.period = 0
			self.off = not self.off
		r = color.r; g = color.g; b = color.b; a = color.a
		if channels[0] and self.off: r = 0
		if channels[1] and self.off: g = 0
		if channels[2] and self.off: b = 0
		if channels[3] and self.off: a = 0
		return Color(r,g,b,a)

TAO = math.pi*2
class Channel_Sin(_Channels):
	def __init__(self):
		self.period = TAO * 0.75
	def tick(self, color, channels, vars=0):
		self.period += vars[0]
		if self.period >= TAO: self.period -= TAO
		r = color.r; g = color.g; b = color.b; a = color.a
		if channels[0]: r *= (math.sin(self.period)+1.3)/2.3
		if channels[1]: g *= (math.sin(self.period)+1.3)/2.3
		if channels[2]: b *= (math.sin(self.period)+1.3)/2.3
		if channels[3]: a *= (math.sin(self.period)+1.3)/2.3
		return Color(r,g,b,a)

class Channel_Random(_Channels):
	def tick(self, color, channels, vars=0):
		r = color.r; g = color.g; b = color.b; a = color.a
		rand = random.random()
		if channels[0]: r *= rand
		if channels[1]: g *= rand
		if channels[2]: b *= rand
		if channels[3]: a *= rand
		return Color(r,g,b,a)

#class Channel_Freeze(_Generators):
#class Channel_Fadeout(_Generators):
#class Channel_Limit(_Generators):

## EOF