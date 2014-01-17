# (c) 2014 Aaron Land - Digital Blacksmith

from piLightsColor import *
import copy, math, random

class _Channels(object):
	def __init__(self):
		self.ON = False
		self.R = True; self.G = True; self.B = True; self.A = False
	def tick(self, color): print 'ERROR _Channels.tick()'; quit()

## CHANNELS @@

class Channel_Blink(_Channels):
	def __init__(self, duration=10):
		super(self.__class__, self).__init__()
		self.duration = duration
		self._period = 0
	def tick(self, color):
		self._period += 1
		if self._period >= self.duration:
			self._period = 0
			self.ON = not self.ON
		r = color.r; g = color.g; b = color.b; a = color.a
		if self.R and not self.ON: r = 0
		if self.G and not self.ON: g = 0
		if self.B and not self.ON: b = 0
		if self.A and not self.ON: a = 0
		return Color(r,g,b,a)

class Channel_Sin(_Channels):
	TAO = math.pi*2
	def __init__(self, delta=0.1):
		super(self.__class__, self).__init__()
		self.delta = delta
		self._period = self.TAO * 0.75
	def tick(self, color):
		self._period += selfl.delta
		if self._period >= self.TAO: self._period -= self.TAO
		r = color.r; g = color.g; b = color.b; a = color.a
		if self.R: r *= (math.sin(self._period)+1.3)/2.3
		if self.G: g *= (math.sin(self._period)+1.3)/2.3
		if self.B: b *= (math.sin(self._period)+1.3)/2.3
		if self.A: a *= (math.sin(self._period)+1.3)/2.3
		return Color(r,g,b,a)

class Channel_Random(_Channels):
	def tick(self, color):
		r = color.r; g = color.g; b = color.b; a = color.a
		if self.R: r = random.randint(0,255)
		if self.G: g = random.randint(0,255)
		if self.B: b = random.randint(0,255)
		if self.A: a = random.randint(0,100)/100.0
		return Color(r,g,b,a)

class Channel_Freeze(_Channels):
	def __init__(self):
		super(self.__class__, self).__init__()
		self.color = Colors.black
	def tick(self, color):
		r = color.r; g = color.g; b = color.b; a = color.a
		if self.R: r = self.color.r
		if self.G: g = self.color.g
		if self.B: b = self.color.b
		if self.A: a = self.color.a
		return Color(r,g,b,a)

class Channel_Fadeout(_Channels):
	def __init__(self, duration=20):
		super(self.__class__, self).__init__()
		self.duration = duration
		self._count = 0
	def tick(self, color):
		self._count -= 1
		if self._count <=0 or self._count > self.duration:
			self._count = self.duration
		fadeOut = self._count/float(self.duration)
		r = color.r; g = color.g; b = color.b; a = color.a
		if self.R: r = r * fadeOut
		if self.G: g = g * fadeOut
		if self.B: b = b * fadeOut
		if self.A: a = a * fadeOut
		return Color(r,g,b,a)

#( http://asliceofraspberrypi.blogspot.com/2013/02/adding-audio-input-device.html )
# class Channel_AudioLevels(_Channels):


## EOF