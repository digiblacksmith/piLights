# (c) 2014 Aaron Land - Digital Blacksmith

from piLightsColor import *
import copy, types, math, random

class _Channels(object):
	def tick(self, color, channels): print 'ERROR'; quit()

## CHANNELS @@

class Channel_Blink(_Channels):
	def __init__(self):
		self.off = True
		self.period = 0
	def tick(self, color, channels, duration=10):
		self.period += 1
		if self.period >= duration:
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
	def tick(self, color, channels, delta=0.1):
		self.period += delta
		if self.period >= TAO: self.period -= TAO
		r = color.r; g = color.g; b = color.b; a = color.a
		if channels[0]: r *= (math.sin(self.period)+1.3)/2.3
		if channels[1]: g *= (math.sin(self.period)+1.3)/2.3
		if channels[2]: b *= (math.sin(self.period)+1.3)/2.3
		if channels[3]: a *= (math.sin(self.period)+1.3)/2.3
		return Color(r,g,b,a)

class Channel_Random(_Channels):
	def tick(self, color, channels):
		r = color.r; g = color.g; b = color.b; a = color.a
		rand = random.random()
		if channels[0]: r *= rand
		if channels[1]: g *= rand
		if channels[2]: b *= rand
		if channels[3]: a *= rand
		return Color(r,g,b,a)

class Channel_Freeze(_Channels):
	def __init__(self):
		self.frozen = Colors.black
	def tick(self, color, channels, newColor=0):
		if newColor: self.frozen = newColor
		r = color.r; g = color.g; b = color.b; a = color.a
		if channels[0]: r = self.frozen.r
		if channels[1]: g = self.frozen.g
		if channels[2]: b = self.frozen.b
		if channels[3]: a = self.frozen.a
		return Color(r,g,b,a)

class Channel_Fadeout(_Channels):
	def __init__(self):
		self.count = 0
	def tick(self, color, channels, duration=20):
		self.count -= 1
		if self.count <=0 or self.count > duration:
			self.count = duration
		fadeOut = self.count/float(duration)
		r = color.r; g = color.g; b = color.b; a = color.a
		if channels[0]: r = r * fadeOut
		if channels[1]: g = g * fadeOut
		if channels[2]: b = b * fadeOut
		if channels[3]: a = a * fadeOut
		return Color(r,g,b,a)


## EOF