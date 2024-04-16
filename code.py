import socket,http.server,json,time,threading
import tkinter as tk
from tkinter import ttk
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

httptxt='Connect To: http://{}:8000'.format( socket.gethostbyname(socket.gethostname()))

class HTTP(http.server.BaseHTTPRequestHandler):
	def do_GET(s):
		s.send_response(200)
		s.end_headers()
		s.wfile.write( bytes(open("console.html").read() , 'UTF-8') )
	def do_POST(s):      
			content_length = int(s.headers['Content-Length'])
			post_data = s.rfile.read(content_length).decode("UTF-8")
			s.send_response(200)
			s.send_header('Content-type','text/html')
			s.end_headers()
			event(json.loads(post_data))
			s.wfile.write(b'done')

win=tk.Tk()
win.title('Console')

ttk.Label(win,text = httptxt,  font = ("Verdana", 15,"bold")).grid(column = 1,  row = 30, padx = 10, pady = 25)

file=json.loads(open('controls.json','r').read())

ttk.Label(win,text = "Button",  font = ("Times New Roman", 10)).grid(column = 0,  row = 45 ,padx = 10, pady = 25)
ttk.Label(win,text = "Key To Be Simulated",  font = ("Times New Roman", 10)).grid(column = 1,  row = 45, padx = 10, pady = 25)

inp={}
i=60
for btn in file:
	
	ttk.Label(win,text = btn+" :",  font = ("Times New Roman", 10)).grid(column = 0,  row = 15+i, padx = 10, pady = 25) 

	inp[btn] = ttk.Combobox(win, width = 10,  textvariable = tk.StringVar()) 
	inp[btn]['values'] = ('w','a','s','d','space','x') 
	inp[btn].current(inp[btn]['values'].index(file[btn]))
	inp[btn].grid(column = 1, row = 15+i)
	i+=15
	
def data_keys():
	json_data={}
	for data in inp:
		json_data[data]=data.get()
	open('controls.json','w').write(json.dumps(json_data))

btn1 = ttk.Button(win, text = 'SAVE',  command = data_keys) 

threading.Thread(target=win.mainloop).start()

http.server.HTTPServer( ('0.0.0.0',8000),HTTP).serve_forever()