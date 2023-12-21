from aiohttp import web
import time
import numpy as np
from pickle import loads ,dumps
import json


async def websocket_handler(request):
    json_mode = False
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    async for msg in ws:
        start_time = time.time()
        if msg.type ==2:
        
            array = loads(msg.data)

            await ws.send_bytes(dumps(array))
        elif msg.type ==1:
            array = msg.data
            await ws.send_json(array)
            
        elapsed_time = time.time() - start_time

    return ws

app = web.Application()
app.add_routes([web.get('/ws', websocket_handler)])

if __name__ == '__main__':
    web.run_app(app, port=8765)
