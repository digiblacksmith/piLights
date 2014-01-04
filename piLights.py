#!/usr/bin/env python
# (c) 2013 Aaron Land - Digital Blacksmith
#
# https://github.com/adammhaile/RPi-LPD8806
# http://tightdev.net/SpiDev_Doc.pdf
# http://learn.adafruit.com/light-painting-with-raspberry-pi/software




def main():
	print "\033[0m!\033[0;31mp\033[0;33mi\033[0;32mL\033[0;33mi\033[0;34mg\033[0;35mh\033[0;36mt\033[0;37ms\033[0;31m!\033[0m"
	print 'Starting webserver...',










"""
from piLightsColor import *
from piLightsLEDstrip import *
from piLightsAnimations import *
from piLightsColorGenerators import *
from piLightsWebserver import *
#import os, sys, time

##

class piLights:
	def __init__(self):
		self.palete = [Colors.orange]
		self.generator = None
		
	def paletteSet(self, palette):
		self.palette = palette
	def paletteAppend(self, color):
		self.palette.append(color)

	def setGenerator(self, id):
		if id == 0:
			self.generator = Gen_Solid(self.palette[0])
		elif id == 1:
			self.generator = Gen_Random()
		elif id == 2:
			self.generator = Gen_RainbowCycle(degree=0.0, delta=0.01)
		elif id == 3:
			self.generator = Gen_DissolveThrough(start=0)
		else:
			self.generator = Gen_Solid(Colors.orange)


## MAIN ##

def main():
	print "\033[0m!\033[0;31mp\033[0;33mi\033[0;32mL\033[0;33mi\033[0;34mg\033[0;35mh\033[0;36mt\033[0;37ms\033[0;31m!\033[0m"
	print 'Starting webserver...',
	piLightsWebserver.Web_Server()

	print 'Running...'

	global gLED, gPiLights
	
	######################
	##  COLOR PALETTE   ##
	######################
	
	#palette = [Color(255,255,0), Color(0,0,255), Color(0,255,255), Color(255,0,0), Color(255,0,255), Color(0,255,0)]
	#palette = [Colors.red, Colors.orange, Colors.yellow, Colors.green, Colors.blue, Colors.indigo, Colors.violet]
	palette = [Hex2Color('FF0000'), Hex2Color('00FF00'), Hex2Color('0000FF')]
	gPiLights.paletteSet(palette)

	#del gPalette[:]
	#gPalette.append(Colors.blue)
	
	######################
	## COLOR GENERATORS ##
	######################

	##	0	Gen_Solid(color)								step()
	##  1	Gen_Random()									step()
	##	2	Gen_RainbowCycle(color,degree=0.0,delta0.01)	step(degree,delta)
	## 	3	Gen_DissolveThrough(start=0)					step(period=10)
	
	gPiLights.setGenerator(2)
	
	## Channel Animations
	#chan_squish = Chan_squish()
	#chan_half = Chan_half()
	#chan_freeze = Chan_freeze(Color(255,0,0))
	#chan_blink = Chan_blink(delay=3)
	#chan_sin = Chan_sin(step=0.1)
	#chan_rand = Chan_Random()
	
	prog_all = Prog_all()
	#prog_cycle = Prog_cycleLinear()

	while True:
		
		color = gPiLights.generator.step()
		#print str(color)
		
		## Channel Patterns
		if 'chan_half' in locals():
			color = chan_half.tick(color, [1,1,1,0])
		if 'chan_freeze' in locals():
			color = chan_freeze.tick(color, [1,1,1,0])
		if 'chan_blink' in locals():
			color = chan_blink.tick(color, [1,0,0,0])
		if 'chan_sin' in locals():
			color = chan_sin.tick(color, [0,0,0,1])
		if 'chan_rand' in locals():
			color = chan_rand.tick(color, [0,0,0,1])
			
		## Apply just before Programs
#		if 'chan_squish' in locals():
#			color = chan_squish.tick(color)

		## Programs
		if 'prog_all' in locals():
			prog_all.run(color)
		elif 'prog_cycle' in locals():
			prog_cycle.run(color, forward=True, fadeOut=0)
		else:
			gLED.fillAll(color)
		
		## Debug
		#print color.r, color.g, color.b, colora
		#printColor(color)

		time.sleep(0.1)

## MAIN

while True:
	try:
		main()
	except (KeyboardInterrupt, SystemExit):
		break

print ''
#gLED.turnAllOff()
print '\033[0mFinished...'

"""