# (c) 2014 Aaron Land - Digital Blacksmith

#( http://www.sessions.edu/color-calculator )
#( http://yuilibrary.com/yui/docs/color/hsl-harmony.html )

## COLOR @@

import math

class Color:
	def __init__(self, r=0,g=0,b=0,a=1.0):
		self.rgba(r,g,b,a)
	def __str__(self):
		return "%d,%d,%d:%.1f" % (self.r,self.g,self.b,self.a)
	def __copy__(self):
		return Color(self.r,self.g,self.b,self.a)
	
	# r=0-255, g=0-255, b=0-255, a=0.0-1.0
	def rgba(self, r,g,b,a=1.0):
		if r < 0: r = 0
		if r > 255: r = 255
		self.r = r
		if g < 0: g = 0
		if g > 255: g = 255
		self.g = g
		if b < 0: b = 0
		if b > 255: b = 255
		self.b = b
		if a < 0.0: a = 0.0
		if a > 1.0: a = 1.0
		self.a = a
	
	#( http://www.cs.rit.edu/~ncs/color/t_convert.html )
	# h=0-360 s=0.0-1.0 v=0.0-1.0 a=0.0-1.0
	def hsva(self, h,s,v,a=1.0):
		if s == 0:
			self.rgba(v,v,v,a)
		h /= 60
		i = math.floor(h)
		f = h - i
		p = v * (1 - s)
		q = v * (1 - s * f)
		t = v * (1 - s * (1 - f))
		
		if i == 0:	self.rgba(v*255,t*255,p*255,a)
		elif i == 1:	self.rgba(q*255,v*255,p*255,a)
		elif i == 2:	self.rgba(p*255,v*255,t*255,a)
		elif i == 3:	self.rgba(p*255,q*255,v*255,a)
		elif i == 4:	self.rgba(t*255,p*255,v*255,a)
		elif i == 5:	self.rgba(v*255,p*255,q*255,a)
		else:		print 'ERROR i=', i; quit()
	
	def add(self, r=0.0,g=0.0,b=0.0,a=0.0):
		self.rgba(self.r+r, self.g+g, self.b+b, self.a+a)
	def multiply(self, r=1.0,g=1.0,b=1.0,a=1.0):
		self.rgba(self.r*r, self.g*g, self.b*b, self.a*a)
	def blend(self, color, percent=1.0):
		r = self.r + (color.r - self.r) * percent
		g = self.g + (color.g - self.g) * percent
		b = self.b + (color.b - self.b) * percent
		self.rgba(r,g,b,self.a)

## COLORS @@

class Colors:
	black	= Color(0,0,0,0)
	white	= Color(255,255,255,1)
	
	red		= Color(255,0,0)
	orange	= Color(255,127,0)
	yellow	= Color(255,255,0)
	green	= Color(0,255,0)
	blue	= Color(0,0,255)
	indigo	= Color(75,0,130)
	violet	= Color(143,0,255)

	on		= Color(255,255,255,0.6)
	off		= black
	error	= Color(255,0,0,0.6)


## COLOR UTILITIES @@

import sys

#def HSVtoColor(h=360,s=1.0,v=1.0,a=1.0):

def Hex2Color(hex, a=1.0):
	hex = hex.strip('#')
	r = int(hex[0:2], 16)
	g = int(hex[2:4], 16)
	b = int(hex[4:6], 16)
	if len(hex) == 8: a = int(hex[6:8], 16) 
	return Color(r,g,b,a)

def Wheel2Color(deg, a=1.0):
	if deg < 0: deg = 0
	if deg > 384: deg = 384
	if deg < 128:
		r = 127 - position % 128; g = position % 128; b = 0
	elif deg < 256:
		g = 127 - position % 128; b = position % 128; r = 0
	else:
		b = 127 - position % 128; r = position % 128; g = 0
	return Color(r, g, b, a)

def printColor(color):
	if color.r >100:
		if color.g >200:
			sys.stdout.write("\033[0;33m. ")	#yellow
			sys.stdout.flush()
			return
		if color.b >100:
			sys.stdout.write("\033[0;35m. ")	#purple
			sys.stdout.flush()
			return
		else:
			sys.stdout.write("\033[0;31m. ")	#red
			sys.stdout.flush()
	elif color.b >100:
		if color.g >100:
			sys.stdout.write("\033[0;36m. ")	#cyan
			sys.stdout.flush()
		else:
			sys.stdout.write("\033[0;34m. ")	#blue
			sys.stdout.flush()
	elif color.g >100:
		sys.stdout.write("\033[0;32m. ")		#green
		sys.stdout.flush()
	elif (color.r + color.g + color.b)/3 > 128:
		sys.stdout.write("\033[0;37m. ")		#white
		sys.stdout.flush()
	else:
		sys.stdout.write("  ")					#black
		sys.stdout.flush()

## EOF @@