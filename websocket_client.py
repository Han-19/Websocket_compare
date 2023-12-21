import asyncio
import websockets
import time
import numpy as np
import pandas as pd
from pickle import dumps, loads
import json

async def benchmark():
    uri = "ws://localhost:8764"
    async with websockets.connect(uri) as ws:

        df = pd.DataFrame([],columns=["elapsed_time","size","iteration_n"])

        for size in range(0,218):
            msg = np.random.random((size, size))
            for iteration in range(32): 
                start_time = time.time()
                await ws.send(dumps(msg))
                array = loads(await  ws.recv())
                elapsed_time = time.time() - start_time
                df.loc[len(df.index)] = [elapsed_time, size,iteration]
        df.to_csv("websocket_test_np2d_bin.csv")     

        df = pd.DataFrame([],columns=["elapsed_time","size","iteration_n"])

        for size in range(0,131052,601):
            msg = np.random.random((size, 1))
            for iteration in range(32): 
                start_time = time.time()
                await ws.send(dumps(msg))
                array = loads(await  ws.recv())
                elapsed_time = time.time() - start_time
                df.loc[len(df.index)] = [elapsed_time, size,iteration ]
        df.to_csv("websocket_test_np1d_bin.csv") 
            
        df = pd.DataFrame([],columns=["elapsed_time","size","iteration_n"])

        for size in range(0,47077,206):

            msg = {}
            msg['key'] = np.random.random((size, 1)).tolist()
            for iteration in range(32): 
                start_time = time.time()
                await ws.send(json.dumps(msg))
                array = json.loads(await  ws.recv())
                elapsed_time = time.time() - start_time
                df.loc[len(df.index)] = [elapsed_time, size,iteration]
        df.to_csv("websocket_test_json1d.csv")
        
        df = pd.DataFrame([],columns=["elapsed_time","size","iteration_n"])
        for size in range(0,228,1):
            msg = {}
            msg['key'] = np.random.random((size, size)).tolist()

            for iteration in range(32): 
                start_time = time.time()
                await ws.send(json.dumps(msg))
                array = json.loads(await  ws.recv())
                elapsed_time = time.time() - start_time
                df.loc[len(df.index)] = [elapsed_time, size,iteration]
        df.to_csv("websocket_test_json2d.csv")
        
asyncio.run(benchmark())
