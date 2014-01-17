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
from piLightsWebsite import *
import time


## PILIGHTS @@

class piLights:
	def __init__(self):
		print "## \033[0m!\033[0;31mp\033[0;33mi\033[0;32mL\033[0;33mi\033[0;34mg\033[0;35mh\033[0;36mt\033[0;37ms\033[0;31m!\033[0m @@"

		#= MASTER =@
		self.LEDs = LEDstrip(28*9, brightness=0.8, console=True)
		self.refresh = 0.05
		
		self.inside = ProgramGroup(28*1, color=Colors.white)
		#self.outside = ProgramGroup(28*2)
		
	def execute(self):
		print 'Running...'
		while True:
			# Inside @
			self.inside.run()
			#self.outside.run()

			# Matrix @
			buff = self.inside.buffer.buffer #+ self.outside.buffer.buffer
			

			# Update @
			self.LEDs.update(buff, scroll=False)
			time.sleep(self.refresh)


if __name__ == "__main__":
	pL = piLights()
	Start_Webserver(pL, console=True)
	try:
		pL.execute()
	except (KeyboardInterrupt, SystemExit):
		print '\033[0m'
	del pL
	print 'Finished...'

## EOF @@