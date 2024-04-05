import socket,http.server,json
from pynput.keyboard import Key,Controller

k=Controller()

def key_set(key):
	f=open("controls.json","r")
	data=json.loads(f.read())
	f.close()
	try:
		return eval("Key."+data[key])
	except :
		return data[key][:1]
    


def event(data):
	if data['e']=="ps":
		k.press( key_set( data['key'] ) )
	if data['e']=="pe":
		k.release( key_set( data['key'] ) )

print('\nConnect To: http://{}:8000\n '.format( socket.gethostbyname(socket.gethostname())))

class HTTP(http.server.BaseHTTPRequestHandler):
	def do_GET(s):
		s.send_response(200)
		s.end_headers()
		s.wfile.write( bytes(open("console.html").read() , 'UTF-8') )
	def do_POST(s):      
			content_length = int(s.headers['Content-Length'])
			post_data = s.rfile.read(content_length).decode("UTF-8")
			print(post_data)
			s.send_response(200)
			s.send_header('Content-type','text/html')
			s.end_headers()
			event(json.loads(post_data))
			s.wfile.write(b'done')

http.server.HTTPServer( ('0.0.0.0',8000),HTTP).serve_forever()