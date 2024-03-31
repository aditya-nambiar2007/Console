from pynput.keyboard import Key,Controller
from socketio  import Server,WSGIApp 
import eventlet,json,file
from socket import gethostbyname as ip

k=Controller()

def press(key):
	k.press(key)
def release(key):
	k.release(key)
	
server=	Server()
app=WSGIApp(server,static_files={'/':'console.html'})

def key_set(key):
	f=file.open("controls.json","r")
	data=json.loads(f.read())
	f.close()
	try:
		a = eval("Key."+data[key])
	except :
		a = data[key][:1]
        return a

@server.on("message")
def event(sid,data):
	if data['e']=="ps":
		press( key_set[ data['key'] ] )
	if data['e']=="pe":
		release( key_set[ data['key'] ] )
pass

print('\n Connect To: http://{}:8000 '.format( ip(hostname) ))
eventlet.wsgi.server(eventlet.listen(("0.0.0.0", 8000)), app)
