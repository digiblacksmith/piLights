# (c) 2014 Aaron Land - Digital Blacksmith

from piLightsColor import *
import copy

## LED STRIP @@

class RGBBuffer:
	def __init__(self, total):
		self.total = total
		self.buffer = [Colors.black for x in range(self.total + 1)]
		#for pixel in range(self.total):
		#	self.buffer[pixel] = Colors.black
	def __add__(self, other):
		return RGBBuffer(self.buffer + other.buffer)

	def turnAllOff(self):
		for pixel in range(self.total):
			self.buffer[pixel] = Colors.black

	def fillAll(self, color, start=0, end=0):
		if start < 0: start = 0
		if end == 0 or end > self.total: end = self.total
		for pixel in range(start, end + 1):
			self.buffer[pixel] = color

	def shiftRight(self, color, start=0, end=0):
		if start < 0: start = 0
		if end == 0 or end > self.total: end = self.total
		for pixel in reversed(range(start+1, end)):
			self.buffer[pixel] = self.buffer[pixel-1]
		self.buffer[start] = color
	def shiftLeft(self, color, start=0, end=0):
		if start < 0: start = 0
		if end == 0 or end > self.total: end = self.total
		for pixel in range(start, end-1):
			self.buffer[pixel] = self.buffer[pixel+1]
		self.buffer[end] = color
#}

class RGBorder:
	RGB=[0,1,2]; GRB=[1,0,2]; BRG=[1,2,0]

class LEDstrip:
	def __init__(self, total, brightness=1.0, order=RGBorder.GRB, console=False):
		if total < 1: total = 1
		self.total = total
		self.brightness = brightness
		self.order = order

		self.console = console
		#self.buffer = RGBBuffer(self.total)

		if not console:
			from LPD8806 import LPD8806
			self.driver = LPD8806(total)

		#( https://sites.google.com/site/mechatronicsguy/lightscythe-v2 )
		self.gamma = bytearray(256)
		for i in range(256):
			self.gamma[i] = 0x80 | int(pow(float(i) / 255.0, 2.5) * 127.0 + 0.5)

	def update(self, buffer, scroll=False):
		if self.console:
			for pixel in range(0, len(buffer)):
				color = buffer[pixel]
				printColor(Color(color.r * color.a * self.brightness,
								 color.g * color.a * self.brightness,
								 color.b * color.a * self.brightness))
			if scroll:	print ''
			else:	print '\033[F'
		else:
			buff = [0 for x in range(self.total + 1)]
			for pixel in range(self.total):
				color = buffer[pixel]
				buff[pixel] = bytearray(3)
				buff[pixel][self.order[0]] = self.gamma[int(color.r * color.a * self.brightness)]
				buff[pixel][self.order[1]] = self.gamma[int(color.g * color.a * self.brightness)]
				buff[pixel][self.order[2]] = self.gamma[int(color.b * color.a * self.brightness)]
			self.driver.update(buff)

## EOF @@