# (c) 2013 Aaron Land - Digital Blacksmith

#( https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest/Synchronous_and_Asynchronous_Requests )

from piLightsColor import *
import web, threading, time

gPiLights = None
gConsole = False
gHTTP = None
gURLs = (
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
	
)

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
		level = float(web.input(level=-1.0).level)
		if level >= 0.0:
			gPiLights.brightness = level/100.0
		print 'LEVEL=', level, int(gPiLights.brightness * 100)
		return int(gPiLights.brightness * 100)

class refresh:
	def GET(self):
		global gPiLights
		rate = float(web.input(rate=-1.0).rate)
		if rate >= 0.0:
			gPiLights.refresh = rate
		print 'RATE=', rate, gPiLights.refresh
		return gPiLights.refresh


# Generators @
class generator:
	def GET(self):
		global gPiLights
		num = int(web.input(num=-1).num)
		if num >= 0:
			gPiLights.setGenerator(num)
		return gPiLights.generator

# http://docs.python.org/2/library/stdtypes.html
# Channels @

my_form = web.form.Form(
	web.form.Checkbox('', id='on'),
	web.form.Checkbox('', id='r'),
	web.form.Checkbox('', id='g'),
	web.form.Checkbox('', id='b'),
	web.form.Textbox('', id='duration'),
)


class chan_blink:
	def GET(self):
		global gPiLights
		str = "%d,%d,%d,%d,%d,%d" %(	gPiLights.chan_Blink[0],
										gPiLights.chan_Blink[2][0],gPiLights.chan_Blink[2][1],gPiLights.chan_Blink[2][2],gPiLights.chan_Blink[2][3],
										gPiLights.chan_Blink[3]);
		print 'GET='+str;
		return str;

	def POST(self):
		global gPiLights
		#print 'POST1=', web.input(on=-1).on, web.input(r=-1).r,web.input(r=-1).g,web.input(r=-1).b, web.input(r=-1).a, web.input(duration=-1).duration
		gPiLights.chan_Blink[0] = web.input(on=False).on
		gPiLights.chan_Blink[2][0] = int(web.input(r=0).r)
		gPiLights.chan_Blink[2][1] = int(web.input(g=0).g)
		gPiLights.chan_Blink[2][2] = int(web.input(b=0).b)
		gPiLights.chan_Blink[2][3] = int(web.input(a=0).a)
		gPiLights.chan_Blink[3] = int(web.input(duration=0).duration)
		print "POST2= %s,%i,%i,%i,%i,%i" % ((gPiLights.chan_Blink[0] == 'True'), int(gPiLights.chan_Blink[2][0]),int(gPiLights.chan_Blink[2][1]),int(gPiLights.chan_Blink[2][2]),int(gPiLights.chan_Blink[2][3]), int(gPiLights.chan_Blink[3]))

class chan_sin:
	def GET(self):
		global gPiLights
		return [ gPiLights.chan_Sin[0], gPiLights.chan_Sin[2], gPiLights.chan_Sin[3] ]

class chan_random:
	def GET(self):
		global gPiLights
		return [ gPiLights.chan_Random[0], gPiLights.chan_Random[2] ]

class chan_freeze:
	def GET(self):
		global gPiLights
		return [ gPiLights.chan_Freeze[0], gPiLights.chan_Freeze[2], gPiLights.chan_Freeze[3], gPiLights.chan_Freeze[4], gPiLights.chan_Freeze[5], gPiLights.chan_Freeze[6] ]

class chan_fadeout:
	def GET(self):
		global gPiLights
		return [ gPiLights.chan_Fadeout[0], gPiLights.chan_Fadeout[2], gPiLights.chan_Fadeout[3] ]


# Programs @



## WEBSITE MAIN @@
class _http_Server(threading.Thread):
	
	def run(self):
		global gURLs
		if gConsole:
			web.internalerror = web.debugerror
		else:
			web.config.debug = False
			#sys.stdout = open('/dev/null', 'w')
		
		app = web.application(gURLs, globals())
		try:
			app.run()
		except:
			print 'Done'

## WEBSITE START @@

def Start_Webserver(pL, console=False):
	global gPiLights, gConsole, gHTTP
	print 'Starting webserver...',
	gPiLights = pL
	gConsole = console
	gHTTP = _http_Server()
	gHTTP.daemon = True
	gHTTP.start()
	time.sleep(1/4.0)

def Stop_Webserver():
	global gHTTP
	gHTTP.shutdown = True
	gHTTP.join()

## EOF @@