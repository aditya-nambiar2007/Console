from pynput.keyboard import Key,Controller
from socketio  import Server,WSGIApp 
import eventlet,json
from socket import gethostbyname, gethostname

k=Controller()

def press(key):
	k.press(key)
def release(key):
	k.release(key)
	
server=	Server()
app=WSGIApp(server,static_files={'/':'console.html'})

def key_set(key):
	f=open("controls.json","r")
	data=json.loads(f.read())
	f.close()
	try:
		return eval("Key."+data[key])
	except :
		return data[key][:1]
    

@server.on("message")
def event(sid,data):
	if data['e']=="ps":
		press( key_set( data['key'] ) )
	if data['e']=="pe":
		release( key_set( data['key'] ) )
pass

print('\nConnect To: http://{}:8000\n '.format( gethostbyname(gethostname())))
eventlet.wsgi.server(eventlet.listen(("0.0.0.0", 8000)), app)