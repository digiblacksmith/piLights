# (c) 2014 Aaron Land - Digital Blacksmith

#! sudo easy_install web.py
#! sudo apt-get install python-webpy
#! sudo pip install web.py

from piLightsColor import *
import time, threading, web

## THREAD MAIN @@
class _http_Server(threading.Thread):
	def __init__(self, console=False):
		super(self.__class__, self).__init__()
		self.console = console

	def run(self):
		import os, sys
		os.chdir('html/')
		urls = (
			## INDEX @@
			'/',				'index',
			'/piLights.css',	'index_css',
			'/piLights.js',		'index_js',

			## MASTER @@
			
			'/brightness',		'brightness',
			'/refresh',			'refresh',

			## INSIDE @@

			# Generators @
			'/in_generator',		'in_generator',
			# Channels @
			'/in_chan_blink',		'in_chan_blink',
			'/in_chan_sin',			'in_chan_sin',
			'/in_chan_random',		'in_chan_random',
			'/in_chan_freeze',		'in_chan_freeze',
			'/in_chan_fadeout',		'in_chan_fadeout',
			# Patterns @
			'/in_patt_all',			'in_patt_all',
			'/in_patt_bitshift',	'in_patt_bitshift',
			
			## OUTSIDE @@
	
			# Generators @
#			'/out_generator',		'out_generator',
			# Channels @
#			'/out_chan_blink',		'out_chan_blink',
#			'/out_chan_sin',		'out_chan_sin',
#			'/out_chan_random',		'out_chan_random',
#			'/out_chan_freeze',		'out_chan_freeze',
#			'/out_chan_fadeout',	'out_chan_fadeout',
			# Patterns @
#			'/out_patt_all',		'out_patt_all',
#			'/out_patt_bitshift',	'out_patt_bitshift',
		)
		if self.console:
			web.internalerror = web.debugerror
		else:
			web.config.debug = False
			sys.stdout = open('/dev/null', 'w')

		app = web.application(urls, globals())
		try:
			app.run()
		except:
			print 'Webserver done.'

## WEBSITE INDEX @@

class index:
	def GET(self):
		return open('index.html', 'r').read()
class index_css:
	def GET(self):
		return open('piLights.css', 'r').read()
class index_js:
	def GET(self):
		return open('piLights.js', 'r').read()

## MASTER CONTROLS @@

class brightness:
	def GET(self):
		global gPiLights
		#print 'BRIGHTNESS_GET=', gPiLights.LEDS.brightness
		return gPiLights.LEDs.brightness

	def POST(self):
		global gPiLights
		#print 'BRIGHTNESS_POST=', float(web.input(level=-1).level)
		gPiLights.LEDs.brightness = float(web.input().level)

class refresh:
	def GET(self):
		global gPiLights
		#print 'REFRESH_GET=', gPiLights.refresh
		return gPiLights.refresh

	def POST(self):
		global gPiLights
		#print 'REFRESH_POST=', float(web.input(rate=-1).rate)
		gPiLights.refresh = float(web.input().rate)

## INSIDE @@

class _inside(object):
	def __init__(self):
		global gPiLights
		self.prog = gPiLights.inside

# Generators @
class in_generator(_inside):
	def GET(self):
		#print 'GEN_GET=', self.prog.generator
		return self.prog.generatorNum

	def POST(self):
		#print 'GEN_POST=', int(web.input(num=-1).num)
		self.prog.generatorNum = int(web.input().num)

# Channels @
class in_chan_blink(_inside):
	def GET(self):
		str = "%s,%d,%d,%d,%d,%d" %(	('True' if self.prog.chan_Blink.ON else 'False'),
										self.prog.chan_Blink.R,self.prog.chan_Blink.G,self.prog.chan_Blink.B,self.prog.chan_Blink.A,
										self.prog.chan_Blink.duration);
		#print 'BLINK_GET=', str;
		return str;

	def POST(self):
		#print 'BLINK_POST1=', web.input(on=-1).on, web.input(r=-1).r,web.input(r=-1).g,web.input(r=-1).b, web.input(r=-1).a, web.input(duration=-1).duration
		input = web.input()
		self.prog.chan_Blink.ON = (input.on == 'True')
		self.prog.chan_Blink.R = int(input.r)
		self.prog.chan_Blink.G = int(input.g)
		self.prog.chan_Blink.B = int(input.a)
		self.prog.chan_Blink.A = int(input.a)
		self.prog.chan_Blink.duration = int(input.duration)
		#print "BLINK_POST2= %s,%i,%i,%i,%i,%i" % (self.prog.chan_Blink.ON, self.prog.chan_Blink.R,self.prog.chan_Blink.G,self.prog.chan_Blink.B,self.prog.chan_Blink.A, self.prog.chan_Blink.duration)

class in_chan_sin(_inside):
	def GET(self):
		str = "%s,%d,%d,%d,%d,%f" %(	('True' if self.prog.chan_Sin.ON else 'False'),
										self.prog.chan_Sin.R,self.prog.chan_Sin.G,self.prog.chan_Sin.B,self.prog.chan_Sin.A,
										self.prog.chan_Sin.delta);
		#print 'SIN_GET=', str;
		return str;

	def POST(self):
		#print 'SIN_POST1=', web.input(on=-1).on, web.input(r=-1).r,web.input(r=-1).g,web.input(r=-1).b, web.input(r=-1).a, web.input(duration=-1).delta
		input = web.input()
		self.prog.chan_Sin.ON = (input.on == 'True')
		self.prog.chan_Sin.R = int(input.r)
		self.prog.chan_Sin.G = int(input.g)
		self.prog.chan_Sin.B = int(input.b)
		self.prog.chan_Sin.A = int(input.a)
		self.prog.chan_Sin.delta = float(input.delta)
		#print "SIN_POST2= %s,%i,%i,%i,%i,%f" % (self.prog.chan_Sin.on, self.prog.chan_Sin.r,self.prog.chan_Sin.g,self.prog.chan_Sin.b,self.prog.chan_Sin.a, self.prog.chan_Sin.delta)

class in_chan_random(_inside):
	def GET(self):
		str = "%s,%d,%d,%d,%d" %(	('True' if self.prog.chan_Random.ON else 'False'),
									self.prog.chan_Random.R,self.prog.chan_Random.G,self.prog.chan_Random.B,self.prog.chan_Random.A,
								);
		#print 'RADNOM_GET=', str;
		return str;

	def POST(self):
		#print 'RANDOM_POST1=', web.input(on=-1).on, web.input(r=-1).r,web.input(r=-1).g,web.input(r=-1).b, web.input(r=-1).a
		input = web.input()
		self.prog.chan_Random.ON = (input.on == 'True')
		self.prog.chan_Random.R = int(input.r)
		self.prog.chan_Random.G = int(input.g)
		self.prog.chan_Random.B = int(input.b)
		self.prog.chan_Random.A = int(input.a)
		#print "RANDOM_POST2= %s,%i,%i,%i,%i" % (self.prog.chan_Random.ON, self.prog.chan_Random.R,self.prog.chan_Random.G,self.prog.chan_Random.B,self.prog.chan_Random.A)

class in_chan_freeze(_inside):
	def GET(self):
		str = "%s,%d,%d,%d,%d" %(	('True' if self.prog.chan_Freeze.ON else 'False'),
									self.prog.chan_Freeze.R,self.prog.chan_Freeze.G,self.prog.chan_Freeze.B,self.prog.chan_Freeze.A,
								);
		#print 'FREEZE_GET=', str;
		return str;

	def POST(self):
		#print 'FREEZE_POST1=', web.input(on=-1).on, web.input(r=-1).r,web.input(r=-1).g,web.input(r=-1).b, web.input(r=-1).a
		input = web.input()
		self.prog.chan_Freeze.ON = (input.on == 'True')
		self.prog.chan_Freeze.R = int(input.r)
		self.prog.chan_Freeze.G = int(input.g)
		self.prog.chan_Freeze.B = int(input.b)
		self.prog.chan_Freeze.A = int(input.a)
		#print "FREEZE_POST2= %s,%i,%i,%i,%i" % (self.prog.chan_Freeze.ON, self.prog.chan_Freeze.R,self.prog.chan_Freeze.G,self.prog.chan_Freeze.B,self.prog.chan_Freeze.A)
		self.prog.chan_Freeze.color = self.prog.color

class in_chan_fadeout(_inside):
	def GET(self):
		str = "%s,%d,%d,%d,%d,%d" %(	('True' if self.prog.chan_Fadeout.ON else 'False'),
										self.prog.chan_Fadeout.R,self.prog.chan_Fadeout.G,self.prog.chan_Fadeout.B,self.prog.chan_Fadeout.A,
										self.prog.chan_Fadeout.duration);
		#print 'FADE_GET=', str;
		return str;

	def POST(self):
		#print 'FADE_POST1=', web.input(on=-1).on, web.input(r=-1).r,web.input(r=-1).g,web.input(r=-1).b, web.input(r=-1).a, web.input(duration=-1).duration
		input = web.input()
		self.prog.chan_Fadeout.ON = (input.on == 'True')
		self.prog.chan_Fadeout.R = int(input.r)
		self.prog.chan_Fadeout.G = int(input.g)
		self.prog.chan_Fadeout.B = int(input.b)
		self.prog.chan_Fadeout.A = int(input.a)
		self.prog.chan_Fadeout.duration = int(input.duration)
		#print "FADE_POST2= %s,%i,%i,%i,%i,%i" % (self.prog.chan_Fadeout.ON, self.prog.chan_Fadeout.R,self.prog.chan_Fadeout.G,self.prog.chan_Fadeout.B,self.prog.chan_Fadeout.A, self.prog.chan_Fadeout.duration)

# Programs @
class in_patt_all(_inside):
	def GET(self):
		str = "%s" %(	('True' if self.prog.patt_All.ON else 'False'));
		#print 'ALL_GET=', str;
		return str;

	def POST(self):
		#print 'ALL_POST1=', web.input(on=-1).on
		self.prog.patt_All.ON = (web.input().on == 'True')
		#print "LR_POST2= %s" % (self.prog.patt_All.ON)

class in_patt_bitshift(_inside):
	def GET(self):
		str = "%s,%d" %(	('True' if self.prog.patt_BitShift.ON else 'False'),
							self.prog.patt_BitShift.direction);
		#print 'SHIFTLR_GET=', str;
		return str;

	def POST(self):
		#print 'LR_POST1=', web.input(on=-1).on, web.input(direction=-1).direction
		input = web.input()
		self.prog.patt_BitShift.ON = (input.on == 'True')
		self.prog.patt_BitShift.direction = int(input.direction)
		#print "LR_POST2= %s,%i" % (self.prog.patt_BitShift.ON,self.prog.patt_BitShift.direction)


## WEBSITE START @@

gPiLights = None
gHTTP = None
def Start_Webserver(pL, console=False):
	global gPiLights, gHTTP
	print 'Starting webserver...',
	gPiLights = pL
	gHTTP = _http_Server(console)
	gHTTP.daemon = True
	gHTTP.start()
	time.sleep(1/2.0)

## EOF @@