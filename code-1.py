from pynput.keyboard import Key,Controller
from socketio  import Server,WSGIApp 
import eventlet

k=Controller()

def press(key):
	k.press(key)
def release(key):
	k.release(key)
	
server=	Server()
app=WSGIApp(server,static_files={'/':'console.html'})

key_set= {
		"Up"  :"w",
		"Left":"a",
		"Right":"d",
		"Down":"s",		
		"X"   :"a",
		"A"   :Key.space,
		"B"   :"d",
		"Y"   :Key.space}

@server.on("message")
def event(sid,data):
	if data['e']=="ps":
		press( key_set[ data['key'] ] )
	if data['e']=="pe":
		release( key_set[ data['key'] ] )
pass

eventlet.wsgi.server(eventlet.listen(("0.0.0.0", 8000)), app)
print("this should not print")
