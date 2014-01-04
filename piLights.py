#!/usr/bin/env python
# (c) 2013 Aaron Land - Digital Blacksmith
#
# https://github.com/adammhaile/RPi-LPD8806
# http://tightdev.net/SpiDev_Doc.pdf
# http://learn.adafruit.com/light-painting-with-raspberry-pi/software

from piLightsLEDstrip import *
from piLightsColor import *
from piLightsGenerators import *
from piLightsChannels import *
from piLightsPrograms import *
import time

## PILIGHTS @@

class piLights:
	def __init__(self, led):
		print "## \033[0m!\033[0;31mp\033[0;33mi\033[0;32mL\033[0;33mi\033[0;34mg\033[0;35mh\033[0;36mt\033[0;37ms\033[0;31m!\033[0m @@"
		
		## LED @@
		self.brightness = 0.8
		self.delay = 0.05
		self.led_count = 28 * 1
		self.led_strip = led
		
		self.led_strip.brightness = self.brightness

		## PALETTE @@
		self.palette = [Color(255,255,0), Color(0,0,255), Color(0,255,255), Color(255,0,0), Color(255,0,255), Color(0,255,0)]
		#self.palette = [Colors.red, Colors.orange, Colors.yellow, Colors.green, Colors.blue, Colors.indigo, Colors.violet]
		#self.palette = [Hex2Color('FF0000'), Hex2Color('00FF00'), Hex2Color('0000FF')]
		#self.palette = [Colors.red, Colors.blue]
		
		## COLOR @@
		self.color = self.palette[0]
		
		## GENERATORS @@		Generators							vars
		self.gen_Constant	= [ Generator_Constant(self.color)				]
		self.gen_Random		= [ Generator_Random()							]
		self.gen_Rainbow	= [ Generator_Rainbow(self.color),		0.01	]
		self.gen_Disolve	= [ Generator_PaletteDisolve(),			10		]
		self.generator = 2

		## CHANELS @@			On/Off	Channels			 r,g,b,a	vars
		self.chan_Blink		= [ False,	Channel_Blink(),	[1,1,1,0],	10		]
		self.chan_Sin		= [ False,	Channel_Sin(),		[1,1,1,0],	0.1		]
		self.chan_Random	= [ False,	Channel_Random(),	[1,1,1,0]			]
		self.chan_Freeze	= [ False,	Channel_Freeze(),	[1,1,1,0],	False	]
		self.chan_Fadeout	= [ False,	Channel_Fadeout(),	[1,1,1,0],	20		]

		## PROGRAMS @@			On/Off	Programs										vars
		self.prog_All		= [ True,	Program_All(self.led_strip, self.color)				]
		self.prog_ShiftLR	= [ False,	Program_ShiftLR(self.led_strip, self.color),	1	]

		print "Loaded!"

	def run(self):
		print 'Running...'
		while True:
			## Generat new color @@
			if self.generator == 0:
				self.color = self.gen_Constant[0].step()
			if self.generator == 1:
				self.color = self.gen_Random[0].step() #(color=)
			if self.generator == 2:
				self.color = self.gen_Rainbow[0].step(delta=self.gen_Rainbow[1])
			if self.generator == 3:
				self.color = self.gen_Disolve[0].step(self.palette, period=self.gen_Disolve[1])

			## Channels @@
			if self.chan_Blink[0]:	self.color = self.chan_Blink[1].tick	(self.color, self.chan_Blink[2], duration=self.chan_Blink[3])
			if self.chan_Sin[0]:	self.color = self.chan_Sin[1].tick		(self.color, self.chan_Sin[2], delta=self.chan_Sin[3])
			if self.chan_Random[0]:	self.color = self.chan_Random[1].tick	(self.color, self.chan_Random[2])
			if self.chan_Freeze[0]:	self.color = self.chan_Freeze[1].tick	(self.color, self.chan_Freeze[2], newColor=0)
			if self.chan_Fadeout[0]:self.color = self.chan_Fadeout[1].tick	(self.color, self.chan_Fadeout[2], duration=20)
			

			## Prorams @@
			if self.prog_All[0] == True:		self.prog_All[1].run(self.color)
			if self.prog_ShiftLR[0] == True:	self.prog_ShiftLR[1].run(self.color, self.prog_ShiftLR[2])
			#if self.prog_DotDance[0] == True:	self.prog_DotDance.run(self.color)

			## Update @@
			self.led_strip.update(ret=False)
			time.sleep(self.delay)

## MAIN @@

if __name__ == "__main__":
	count = 28 * 1
	
	c = Colors.blue
	
	LEDs = LEDstrip(count, console=True)
	pL = piLights(LEDs)
	
	#print 'Starting webserver...',
	#web = Start_Webserver(console=True)
	
	try:
		pL.run()
	except (KeyboardInterrupt, SystemExit):
		print '\033[0m'

	LEDs.turnAllOff()
	print 'Finished...'

## EOF @@