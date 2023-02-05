const ws=io('ws://localhost:100')
ws.emit('data')
let controls={
    press_start:f=>ws.on('ps',f),
    press_end:f=>ws.on('pe',f),
    start:f=>ws.on('start',f)
}