# (c) 2013 Aaron Land - Digital Blacksmith

from piLightsColor import *
import web, threading, time

gPiLights = None
gConsole = False
gHTTP = None
gURLs = (
	## index
	'/',				'index',
	'/piLights.css',	'index_css',
	'/piLights.js',		'index_js',

	## Master
	'/brightness',		'brightness',
	'/refresh',			'refresh',
	
	
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

## Master
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



## WEBSITE MAIN @@
class _http_Server(threading.Thread):
	
	def run(self):
		global gURLs
		web.internalerror = web.debugerror
		app = web.application(gURLs, globals())
		if not gConsole:
			sys.stdout = open('/dev/null', 'w')
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