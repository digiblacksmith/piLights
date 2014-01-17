# (c) 2014 Aaron Land - Digital Blacksmith

from piLightsColor import *
from piLightsLEDstrip import *
from piLightsGenerators import *
from piLightsChannels import *
from piLightsPatterns import *
import copy

class ProgramGroup(object):
	def __init__(self, total, color=Colors.black):
		self.buffer = RGBBuffer(total)
		self.color = color
		
		# GENERATORS @
		self.gen_Constant	= Generator_Constant(self.color)
		self.gen_Random		= Generator_Random()
		self.gen_Rainbow	= Generator_Rainbow(self.color, 0.01)
		self.gen_Disolve	= Generator_PaletteDissolve(10, [Colors.red, Colors.green, Colors.blue])
		self.gen_Webcam		= Generator_WebCam()
		self.generatorNum = 0

		# CHANELS @
		self.chan_Blink		= Channel_Blink(10)
		self.chan_Sin		= Channel_Sin(0.1)
		self.chan_Random	= Channel_Random()
		self.chan_Freeze	= Channel_Freeze()
		self.chan_Fadeout	= Channel_Fadeout(20)

		# PATTERNS @
		self.patt_All		= Pattern_All(self.buffer, on=True)
		self.patt_BitShift	= Pattern_BitShift(self.buffer, 1)
		self.patternNum = 0

	def run(self):
		# Generate new color @
		if   self.generatorNum == 1:	self.color = self.gen_Random.step()
		elif self.generatorNum == 2:	self.color = self.gen_Rainbow.step()
		elif self.generatorNum == 3:	self.color = self.gen_Disolve.step()
		elif self.generatorNum == 4:	self.color = self.gen_Webcam.step()
		else: 							self.color = self.gen_Constant.step()
		
		# Channel manipulators @
		if self.chan_Blink.ON:		self.color = self.chan_Blink.tick(self.color)
		if self.chan_Sin.ON:		self.color = self.chan_Sin.tick(self.color)
		if self.chan_Random.ON:		self.color = self.chan_Random.tick(self.color)
		if self.chan_Freeze.ON:		self.color = self.chan_Freeze.tick(self.color)
		if self.chan_Fadeout.ON:	self.color = self.chan_Fadeout.tick(self.color)

		# Patterns @
		if self.patt_BitShift.ON:	self.patt_BitShift.run(self.color)
		if self.patt_All.ON:		self.patt_All.run(self.color)

## EOF
