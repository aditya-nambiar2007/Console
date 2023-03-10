const http = require('http').createServer(function (req, res) {
    require('fs').readFile('console.html', function(err, data) {
      res.writeHead(200, {'Content-Type': 'text/html'});
      res.write(data);
      return res.end();
    });
  });
let players={}
const io = require('socket.io')(http, { cors: { origin: "*" } });

io.on('connection', (socket) => {
    let id;
    socket.on('d',m=>{
        if(!players.hasOwnProperty(m)){players[m]=m; id=m}
    })
    socket.on('data',m=>{
      let people=[]
        for (const key in players) {
          people.push(key)
        }
         socket.emit('start',people)    
        })

    socket.on('message', (message) =>     {
    console.log(message);
     io.emit(message.e , message );   
    });
    socket.on('disconnect',()=>{delete players[id]})
});

let ip=[]
let os=require('os').networkInterfaces()
for (const k in os) {
os[k].forEach(e=>{
  if(e.family=='IPv4'){
    ip.push(e.address)}
})

}
http.listen(100, () => console.log(`CONNECT TO: http://${ip[0]}:100`) );