import socket,json,threading,urllib.request ,os.path
from socketio import WSGIApp,Server
import eventlet
import tkinter as tk
from tkinter import ttk
from pynput.keyboard import Controller

for file in ['console.html','socket.io.min.js','icon.ico','controls.json']:
	if not os.path.isfile(file):
		urllib.request.urlretrieve('https://raw.githubusercontent.com/aditya-nambiar2007/Console/main/'+file, file	)

k=Controller()
keys=("alt","alt_gr","alt_l","alt_r","backspace","caps_lock","cmd","cmd_l","cmd_r","ctrl","ctrl_l","ctrl_r","delete","down","end","enter","esc","f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12","home","insert","left","media_next","media_play_pause","media_previous","media_volume_down","media_volume_mute","media_volume_up","menu","num_lock","page_down","page_up","pause","print_screen","right","scroll_lock","shift","shift_l","shift_r","space","tab","up",'a', 'b','c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's','t', 'u', 'v', 'w', 'x', 'y', 'z','1','2','3','4','5','6','7','8','9','0','!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '-', '.', '~', '|', '<', '>', '=', '-', '_', '/', ':', ';', '?', '[', ']', '{', '}', '~') 

def list_filter(e):
	value=e.widget.get()
	e.widget['values']=tuple( filter( lambda x:	x.startswith(value) ,keys) )

f=open("controls.json","r")
data_keyvals=json.loads(f.read())
f.close()


def key_set(key):
	try:
		return eval("Key."+data_keyvals[key])
	except :
		return data_keyvals[key][:1]


httptxt='Connect To: http://{}:8000'.format( socket.gethostbyname(socket.gethostname()))

server=Server()
app=WSGIApp(server,static_files={'/':'console.html','/socket.io.min.js':'socket.io.min.js'})
@server.on("event")
def event(sid,data):
	data=json.loads(data)
	if data['e']=="ps":
		k.press( key_set( data['key'] ) )
	if data['e']=="pe":
		k.release( key_set( data['key'] ) )

def serve():
    global http_server
    http_server = eventlet.listen(("0.0.0.0", 8000))
    eventlet.wsgi.server(http_server, app)
threading.Thread(target=serve, daemon=True).start()	
print('\nPlease Close The Server Window After Console Is Used\n')

win=tk.Tk()
win.title('Console')
win.iconbitmap("icon.ico")

ttk.Label(win,text = httptxt,  font = ("Verdana", 15,"bold")).grid(column = 1,  row = 30, padx = 10, pady = 5)

file=json.loads(open('controls.json','r').read())

ttk.Label(win,text = "Button",  font = ("Times New Roman", 10)).grid(column = 0,  row = 45 ,padx = 10, pady = 5)
ttk.Label(win,text = "Key To Be Simulated",  font = ("Times New Roman", 10)).grid(column = 1,  row = 45, padx = 10, pady = 5)

inp={}
i=60
for btn in file:
	ttk.Label(win,text = btn+" :",  font = ("Times New Roman", 10)).grid(column = 0,  row = 15+i, padx = 10, pady = 5) 	
	inp[btn] = ttk.Combobox(win, width = 20,  textvariable = tk.StringVar()) 
	inp[btn]['values'] = keys
	inp[btn].current(inp[btn]['values'].index(file[btn]))
	inp[btn].bind('<KeyRelease>',list_filter)
	inp[btn].grid(column = 1, row = 15+i)
	i+=15
	
def data_keys():
	global data_keyvals
	json_data={}
	for data in inp:
		json_data[data]=inp[data].get()
	open('controls.json','w').write(json.dumps(json_data))
	data_keyvals=json_data

def close():
	eventlet.greenthread.spawn(eventlet.wsgi.server,http_server,app)
	win.destroy()

btn1 = ttk.Button(win, text = 'SAVE',  command = data_keys).grid(column=1,row=30+i)
win.protocol("WM_DELETE_WINDOW",close)
win.mainloop()