from bottle import Bottle, run
import waitress
import web
import db
from threading import *
import time
import os
from doreah.settings import get_settings
from doreah import auth
#import auth
import signal


HOST, PORT = get_settings("HOST","PORT")
THREADS = 12




#db.load_database()
db.scan_new()
db.prune_database()



def graceful_exit(sig=None,frame=None):
	print("Server shutting down...")
	db.save_database()
	os._exit(42)

signal.signal(signal.SIGINT, graceful_exit)
signal.signal(signal.SIGTERM, graceful_exit)


server = Bottle()

db.api.mount(server=server)
auth.authapi.mount(server=server)
web.server_handlers(server=server)

#run(server, host='::', port=PORT, server='waitress',threads=24)
waitress.serve(server,host=HOST,port=PORT,threads=THREADS)
