# (c) 2014 Aaron Land - Digital Blacksmith

#from LPD8806 import LPD8806
from piLightsColor import *
import copy

## LED STRIP @@

class RGBorder:
	RGB=[0,1,2]; GRB=[1,0,2]; BRG=[1,2,0]

class LEDstrip:
	def __init__(self, total, use_spidev=False, dev='/dev/spidev0.0', order=RGBorder.GRB, console=False):
		if total < 1: total = 1
		self.total = total
		self.order = order
		self.brightness = 1.0
		self.console = console
		self.buffer = [0 for x in range(total + 1)]
		for pixel in range(self.total):
			self.buffer[pixel] = bytearray(3)
				
		if not console:
			import LPD8806
			self.driver = LPD8806(total, use_spidev, dev)
			#( https://sites.google.com/site/mechatronicsguy/lightscythe-v2 )
		
		self.gamma = bytearray(256)
		for i in range(256):
			if console:
				self.gamma[i] = i
			else:
				self.gamma[i] = 0x80 | int(pow(float(i) / 255.0, 2.5) * 127.0 + 0.5)
		
		self.turnAllOff()
		
	def setOrder(self, order):
		self.order = order
	def setBrightness(self, level):
		if level < 0.0: level = 0.0
		if level > 1.0: level = 1.0
		self.brightness = level

	def turnOff(self, pixel):
		self.set(pixel, Colors.black)
	def turnAllOff(self):
		for pixel in range(self.total):
			self.turnOff(pixel)
		self.update()

	def set(self, pixel, color):
		if pixel < 0: pixel = 0;
		if pixel >= self.total: pixel = self.total-1
		#print pixel, color
		self.buffer[pixel][self.order[0]] = int(color.r * color.a)
		self.buffer[pixel][self.order[1]] = int(color.g * color.a)
		self.buffer[pixel][self.order[2]] = int(color.b * color.a)

	def fillAll(self, color, start=0, end=0):
		if start < 0: start = 0
		if end == 0 or end > self.total: end = self.total
		for pixel in range(start, end + 1):
			self.set(pixel, color)

	def shiftRight(self, color, start=0, end=0):
		if start < 0: start = 0
		if end == 0 or end > self.total: end = self.total
		for pixel in reversed(range(start+1, end)):
			self.buffer[pixel][self.order[0]] = self.buffer[pixel-1][self.order[0]]
			self.buffer[pixel][self.order[1]] = self.buffer[pixel-1][self.order[1]]
			self.buffer[pixel][self.order[2]] = self.buffer[pixel-1][self.order[2]]
		self.set(start, color)
	def shiftLeft(self, color, start=0, end=0):
		if start < 0: start = 0
		if end == 0 or end > self.total: end = self.total
		for pixel in range(start, end-1):
			self.buffer[pixel][self.order[0]] = self.buffer[pixel+1][self.order[0]]
			self.buffer[pixel][self.order[1]] = self.buffer[pixel+1][self.order[1]]
			self.buffer[pixel][self.order[2]] = self.buffer[pixel+1][self.order[2]]
		self.set(end, color)

	def update(self, ret=False):
		buff = [0 for x in range(self.total + 1)]
		for pixel in range(self.total):
			buff[pixel] = bytearray(3)
			buff[pixel][self.order[0]] = self.gamma[int(self.buffer[pixel][self.order[0]] * self.brightness)]
			buff[pixel][self.order[1]] = self.gamma[int(self.buffer[pixel][self.order[1]] * self.brightness)]
			buff[pixel][self.order[2]] = self.gamma[int(self.buffer[pixel][self.order[2]] * self.brightness)]
		if self.console:
			for pixel in range(0, self.total):
				printColor(Color(buff[pixel][self.order[0]],buff[pixel][self.order[1]],buff[pixel][self.order[2]]))
			if ret:	print ''
			else:	print '\033[F'
		else:
			self.driver.update(buff)

## EOF @@