# (c) 2014 Aaron Land - Digital Blacksmith

#! sudo easy_install web.py
#! sudo apt-get install python-webpy
#! sudo pip install web.py

from piLightsColor import *
import web, threading, time

## THREAD MAIN @@
class _http_Server(threading.Thread):
	def __init__(self, console=False):
		super(self.__class__, self).__init__()
		self.console = console

	def run(self):
		urls = (
			# index @
			'/',				'index',
			'/piLights.css',	'index_css',
			'/piLights.js',		'index_js',

			# Master @
			'/brightness',		'brightness',
			'/refresh',			'refresh',
	
			# Generators @
			'/generator',		'generator',
	
			# Channels @
			'/chan_blink',		'chan_blink',
			'/chan_sin',		'chan_sin',
			'/chan_random',		'chan_random',
			'/chan_freeze',		'chan_freeze',
			'/chan_fadeout',	'chan_fadeout',
	
			# Programs @
			'/prog_all',		'prog_all',
			'/prog_shiftLR',	'prog_shiftLR',
	
		)
		if self.console:
			web.internalerror = web.debugerror
		else:
			web.config.debug = False
			#sys.stdout = open('/dev/null', 'w')
		
		app = web.application(urls, globals())
		try:
			app.run()
		except:
			print 'Done'

## WEBSITE INDEX @@

class index:
	def GET(self):
		return open('html/index.html', 'r').read()
class index_css:
	def GET(self):
		return open('html/piLights.css', 'r').read()
class index_js:
	def GET(self):
		return open('html/piLights.js', 'r').read()

## WEBSITE CONTROLS @@


# Master @
class brightness:
	def GET(self):
		global gPiLights
		#print 'LEVEL_GET=', int(gPiLights.brightness * 100)
		return int(gPiLights.brightness * 100)

	def POST(self):
		global gPiLights
		#print 'LEVEL_POST=', float(web.input(level=-1).level)/100.0
		gPiLights.brightness = float(web.input().level)/100.0

class refresh:
	def GET(self):
		global gPiLights
		#print 'RATE_GET=', gPiLights.refresh
		return gPiLights.refresh

	def POST(self):
		global gPiLights
		#print 'RATE_POST=', float(web.input(rate=-1).rate)
		gPiLights.refresh = float(web.input().rate)

# Generators @
class generator:
	def GET(self):
		global gPiLights
		#print 'GEN_GET=', gPiLights.generator
		return gPiLights.generator

	def POST(self):
		global gPiLights
		#print 'GEN_POST=', int(web.input(num=-1).num)
		gPiLights.setGenerator(int(web.input().num))

# Channels @
class chan_blink:
	def GET(self):
		global gPiLights
		str = "%s,%d,%d,%d,%d,%d" %(	('True' if gPiLights.chan_Blink[0] else 'False'),
										gPiLights.chan_Blink[2][0],gPiLights.chan_Blink[2][1],gPiLights.chan_Blink[2][2],gPiLights.chan_Blink[2][3],
										gPiLights.chan_Blink[3]);
		#print 'BLINK_GET=', str;
		return str;

	def POST(self):
		global gPiLights
		#print 'BLINK_POST1=', web.input(on=-1).on, web.input(r=-1).r,web.input(r=-1).g,web.input(r=-1).b, web.input(r=-1).a, web.input(duration=-1).duration
		gPiLights.chan_Blink[0] = (web.input().on == 'True')
		gPiLights.chan_Blink[2][0] = int(web.input().r)
		gPiLights.chan_Blink[2][1] = int(web.input().g)
		gPiLights.chan_Blink[2][2] = int(web.input().b)
		gPiLights.chan_Blink[2][3] = int(web.input().a)
		gPiLights.chan_Blink[3] = int(web.input().duration)
		#print "BLINK_POST2= %s,%i,%i,%i,%i,%i" % (gPiLights.chan_Blink[0], gPiLights.chan_Blink[2][0],gPiLights.chan_Blink[2][1],gPiLights.chan_Blink[2][2],gPiLights.chan_Blink[2][3], gPiLights.chan_Blink[3])

class chan_sin:
	def GET(self):
		global gPiLights
		str = "%s,%d,%d,%d,%d,%f" %(	('True' if gPiLights.chan_Sin[0] else 'False'),
										gPiLights.chan_Sin[2][0],gPiLights.chan_Sin[2][1],gPiLights.chan_Sin[2][2],gPiLights.chan_Sin[2][3],
										gPiLights.chan_Sin[3]);
		#print 'SIN_GET=', str;
		return str;

	def POST(self):
		global gPiLights
		#print 'SIN_POST1=', web.input(on=-1).on, web.input(r=-1).r,web.input(r=-1).g,web.input(r=-1).b, web.input(r=-1).a, web.input(duration=-1).delta
		gPiLights.chan_Sin[0] = (web.input().on == 'True')
		gPiLights.chan_Sin[2][0] = int(web.input().r)
		gPiLights.chan_Sin[2][1] = int(web.input().g)
		gPiLights.chan_Sin[2][2] = int(web.input().b)
		gPiLights.chan_Sin[2][3] = int(web.input().a)
		gPiLights.chan_Sin[3] = float(web.input().delta)
		#print "SIN_POST2= %s,%i,%i,%i,%i,%f" % (gPiLights.chan_Sin[0], gPiLights.chan_Sin[2][0],gPiLights.chan_Sin[2][1],gPiLights.chan_Sin[2][2],gPiLights.chan_Sin[2][3], gPiLights.chan_Sin[3])

class chan_random:
	def GET(self):
		global gPiLights
		str = "%s,%d,%d,%d,%d" %(	('True' if gPiLights.chan_Random[0] else 'False'),
									gPiLights.chan_Random[2][0],gPiLights.chan_Random[2][1],gPiLights.chan_Random[2][2],gPiLights.chan_Random[2][3],
								);
		#print 'RADNOM_GET=', str;
		return str;

	def POST(self):
		global gPiLights
		#print 'RANDOM_POST1=', web.input(on=-1).on, web.input(r=-1).r,web.input(r=-1).g,web.input(r=-1).b, web.input(r=-1).a
		gPiLights.chan_Random[0] = (web.input().on == 'True')
		gPiLights.chan_Random[2][0] = int(web.input().r)
		gPiLights.chan_Random[2][1] = int(web.input().g)
		gPiLights.chan_Random[2][2] = int(web.input().b)
		gPiLights.chan_Random[2][3] = int(web.input().a)
		#print "RANDOM_POST2= %s,%i,%i,%i,%i" % (gPiLights.chan_Random[0], gPiLights.chan_Random[2][0],gPiLights.chan_Random[2][1],gPiLights.chan_Random[2][2],gPiLights.chan_Random[2][3])
		####gPiLights.chan_Random[1].update(gPiLights.color)

class chan_freeze:
	def GET(self):
		global gPiLights
		str = "%s,%d,%d,%d,%d" %(	('True' if gPiLights.chan_Freeze[0] else 'False'),
									gPiLights.chan_Freeze[2][0],gPiLights.chan_Freeze[2][1],gPiLights.chan_Freeze[2][2],gPiLights.chan_Freeze[2][3],
								);
		#print 'FREEZE_GET=', str;
		return str;

	def POST(self):
		global gPiLights
		#print 'FREEZE_POST1=', web.input(on=-1).on, web.input(r=-1).r,web.input(r=-1).g,web.input(r=-1).b, web.input(r=-1).a
		gPiLights.chan_Freeze[0] = (web.input().on == 'True')
		gPiLights.chan_Freeze[2][0] = int(web.input().r)
		gPiLights.chan_Freeze[2][1] = int(web.input().g)
		gPiLights.chan_Freeze[2][2] = int(web.input().b)
		gPiLights.chan_Freeze[2][3] = int(web.input().a)
		#print "FREEZE_POST2= %s,%i,%i,%i,%i" % (gPiLights.chan_Freeze[0], gPiLights.chan_Freeze[2][0],gPiLights.chan_Freeze[2][1],gPiLights.chan_Freeze[2][2],gPiLights.chan_Freeze[2][3])
		gPiLights.chan_Freeze[1].color = gPiLights.color

class chan_fadeout:
	def GET(self):
		global gPiLights
		str = "%s,%d,%d,%d,%d,%d" %(	('True' if gPiLights.chan_Fadeout[0] else 'False'),
										gPiLights.chan_Fadeout[2][0],gPiLights.chan_Fadeout[2][1],gPiLights.chan_Fadeout[2][2],gPiLights.chan_Fadeout[2][3],
										gPiLights.chan_Fadeout[3]);
		#print 'FADE_GET=', str;
		return str;

	def POST(self):
		global gPiLights
		#print 'FADE_POST1=', web.input(on=-1).on, web.input(r=-1).r,web.input(r=-1).g,web.input(r=-1).b, web.input(r=-1).a, web.input(duration=-1).duration
		gPiLights.chan_Fadeout[0] = (web.input().on == 'True')
		gPiLights.chan_Fadeout[2][0] = int(web.input().r)
		gPiLights.chan_Fadeout[2][1] = int(web.input().g)
		gPiLights.chan_Fadeout[2][2] = int(web.input().b)
		gPiLights.chan_Fadeout[2][3] = int(web.input().a)
		gPiLights.chan_Fadeout[3] = int(web.input().duration)
		#print "FADE_POST2= %s,%i,%i,%i,%i,%i" % (gPiLights.chan_Fadeout[0], gPiLights.chan_Fadeout[2][0],gPiLights.chan_Fadeout[2][1],gPiLights.chan_Fadeout[2][2],gPiLights.chan_Fadeout[2][3], gPiLights.chan_Fadeout[3])
		gPiLights.chan_Fadeout[1].duration = gPiLights.chan_Fadeout[3]

# Programs @
class prog_all:
	def GET(self):
		global piLights
		str = "%s" %(	('True' if gPiLights.prog_All[0] else 'False'));
		#print 'ALL_GET=', str;
		return str;

	def POST(self):
		global gPiLights
		#print 'ALL_POST1=', web.input(on=-1).on
		gPiLights.prog_All[0] = (web.input().on == 'True')
		#print "LR_POST2= %s" % (gPiLights.prog_All[0])

class prog_shiftLR:
	def GET(self):
		global piLights
		str = "%s,%d" %(	('True' if gPiLights.prog_ShiftLR[0] else 'False'),
										gPiLights.prog_ShiftLR[2]);
		#print 'SHIFTLR_GET=', str;
		return str;

	def POST(self):
		global gPiLights
		#print 'LR_POST1=', web.input(on=-1).on, web.input(r=-1).length
		gPiLights.prog_ShiftLR[0] = (web.input().on == 'True')
		gPiLights.prog_ShiftLR[2] = int(web.input().length)
		#print "LR_POST2= %s,%i" % (gPiLights.prog_ShiftLR[0],gPiLights.prog_ShiftLR[2])


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

def Stop_Webserver():
	global gHTTP
	gHTTP.shutdown = True
	gHTTP.join()

## EOF @@