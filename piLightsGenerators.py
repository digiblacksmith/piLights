# (c) 2014 Aaron Land - Digital Blacksmith

from piLightsColor import *
import copy, types, random, colorsys, os, threading, time

class _Generators(object):
	def step(self): print 'ERROR'; quit()

## GENERATORS @@

# Constant @
class Generator_Constant(_Generators):
	def __init__(self, color):
		self.frozen = copy.copy(color)
	def step(self, color=0):
		if type(color) is types.InstanceType:
			self.frozen = copy.copy(color)
		return copy.copy(self.frozen)

# Random @
class Generator_Random(_Generators):
	def step(self, color=0):
		ranc = Color(random.randrange(0, 256, 1),random.randrange(0, 256, 1),random.randrange(0, 256, 1))
		if type(color) is types.InstanceType:
			ranc.multiply(color.r,color,g,color.b,color.a)
		return ranc

# Rainbow @
class Generator_Rainbow(_Generators):
	def __init__(self, color):
		super(self.__class__, self).__init__()
		self.update(color)
		
	def update(self, color):
		self.degree, l, s = colorsys.rgb_to_hls(color.r/255.0, color.g/255.0, color.b/255.0)
		
	def step(self, color=0, delta=0.01):
		if type(color) is types.InstanceType:
			self.degree, l, s = colorsys.rgb_to_hls(color.r/255.0, color.g/255.0, color.b/255.0)
		self.degree += delta
		if self.degree >= 1.0: self.degree -= 1.0
		if self.degree < 0.0: self.degree += 1.0
		r, g, b = colorsys.hls_to_rgb(self.degree, 0.5, 1.0)
		return Color(r*255,g*255,b*255)

# Palette rotate disolve
class Generator_PaletteDisolve(_Generators):
	def __init__(self):
		super(self.__class__, self).__init__()
		self.palette_index = 0
		self.period_count = 0

	def step(self, palette, period=10):
		pal_len = len(palette)
		if pal_len == 1:
			return palette[0]

		self.period_count += 1
		if self.period_count >= period:
			self.period_count = 0
			self.palette_index += 1
			if self.palette_index >= pal_len:
				self.palette_index = 0

		color_from = copy.copy(palette[self.palette_index])
		index_next = self.palette_index + 1
		if index_next >= pal_len:
			index_next = 0
		color_to = palette[index_next]
		color_from.blend(color_to, self.period_count/float(period))
		return color_from

# Webcam input @
class _Webcam(threading.Thread):
	def __init__(self):
		super(self.__class__, self).__init__()
		self.palette = [Color(0,0,0)]
	
	def run(self):
		import cv2
		cam = cv2.VideoCapture(0)
		while True:
			GRIDSIZE = 8
			
			# Campture image
			s, img = cam.read()
			# Scale
			grid = cv2.resize(img, (GRIDSIZE,GRIDSIZE))
			#cv2.imwrite('img.jpg', grid)
			
			# Find average color
			R=G=B=0
			sample_div = 1/float(GRIDSIZE*GRIDSIZE)
			for x in xrange(GRIDSIZE):
				for y in xrange(GRIDSIZE):
					b,g,r = grid[x,y]
					R += r * sample_div
					G += g * sample_div
					B += b * sample_div
			m = 254/max(R,G,B)/2
			self.palette = [Color(R*m,G*m,B*m)]
			time.sleep(0.1)

class Generator_WebCam(_Generators):
	def __init__(self):
		super(self.__class__, self).__init__()
		self.on = os.path.exists('/dev/video0')
		if self.on:
			self.thread = _Webcam()
			self.thread.daemon = True
			self.thread.start()
			time.sleep(2)

	def step(self):
		if self.on:
			return self.thread.palette[0]
		return Color(0,0,0)




## EOF