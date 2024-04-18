import socket,http.server,json,time,multiprocessing
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
		return (data[key] or 'x')[:1]

def event(data):
	if data['e']=="ps":
		k.press( key_set( data['key'] ) )
	if data['e']=="pe":
		k.release( key_set( data['key'] ) )

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

httptxt='Connect To: http://{}:8000'.format( socket.gethostbyname(socket.gethostname()))
ttk.Label(win,text = httptxt,  font = ("Verdana", 15,"bold")).grid(column = 1,  row = 30, padx = 10, pady = 5)

file=json.loads(open('controls.json','r').read())

ttk.Label(win,text = "Button",  font = ("Times New Roman", 10)).grid(column = 0,  row = 45 ,padx = 10, pady = 5)
ttk.Label(win,text = "Key To Be Simulated",  font = ("Times New Roman", 10)).grid(column = 1,  row = 45, padx = 10, pady = 5)

inp={}
i=60
for btn in file:
	ttk.Label(win,text = btn+" :",  font = ("Times New Roman", 10)).grid(column = 0,  row = 15+i, padx = 10, pady = 5) 
	
	inp[btn] = ttk.Combobox(win, width = 20,  textvariable = tk.StringVar()) 
	inp[btn]['values'] = ("alt","alt_gr","alt_l","alt_r","backspace","caps_lock","cmd","cmd_l","cmd_r","ctrl","ctrl_l","ctrl_r","delete","down","end","enter","esc","f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12","home","insert","left","media_next","media_play_pause","media_previous","media_volume_down","media_volume_mute","media_volume_up","menu","num_lock","page_down","page_up","pause","print_screen","right","scroll_lock","shift","shift_l","shift_r","space","tab","up",'a', 'b','c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's','t', 'u', 'v', 'w', 'x', 'y', 'z','1','2','3','4','5','6','7','8','9','0','!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '-', '.', '~', '|', '<', '>', '=', '-', '_', '/', ':', ';', '?', '[', ']', '{', '}', '~') 
	inp[btn].current(inp[btn]['values'].index(file[btn]))
	inp[btn].grid(column = 1, row = 15+i)
	i+=15
	
def data_keys():
	json_data={}
	for data in inp:
		json_data[data]=data.get(1)
	open('controls.json','w').write(json.dumps(json_data))

btn1 = ttk.Button(win, text = 'SAVE',  command = data_keys).grid(column=1,row=30+i)

proc=multiprocessing.Process(target=http.server.HTTPServer( ('0.0.0.0',8000),HTTP).serve_forever).start()
proc.start()
def closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        proc.terminate()

root.protocol("WM_DELETE_WINDOW",closing)
win.mainloop()