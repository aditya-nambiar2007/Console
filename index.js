const http = require('http').createServer(function (req, res) {
    require('fs').readFile('demofile1.html', function(err, data) {
      res.writeHead(200, {'Content-Type': 'text/html'});
      res.write(data);
      return res.end();
    });
  });
let players=[]
const io = require('socket.io')(http, { cors: { origin: "*" } });

io.on('connection', (socket) => {
    socket.on('d',m=>{
        if(!players.includes(m)){players.push(m)}
    })
    socket.on('data',m=>{   socket.emit('start',players)    })

    socket.on('message', (message) =>     {
     io.emit(message.e , message );   
    });
});

http.listen(100, () => console.log(`http://${require('ip').address()}:100`) );
