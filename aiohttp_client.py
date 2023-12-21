import aiohttp
import asyncio
import time
import numpy as np
import json
from pickle import dumps, loads
import pandas as pd


async def benchmark():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('http://localhost:8765/ws') as ws:

            df = pd.DataFrame([],columns=["elapsed_time","size","iteration_n"])

            for size in range(0,724):
                msg = np.random.random((size, size))
                for iteration in range(32): 
                    start_time = time.time()
                    await ws.send_bytes(dumps(msg))
                    array = loads(await  ws.receive_bytes())
                    elapsed_time = time.time() - start_time
                    df.loc[len(df.index)] = [elapsed_time, size,iteration]
            df.to_csv("aiohttp_np2d.csv")     
            df = pd.DataFrame([],columns=["elapsed_time","size","iteration_n"])
            
            for size in range(0,524268,724):
                msg = np.random.random((size, 1))
                for iteration in range(32): 
                    start_time = time.time()
                    await ws.send_bytes(dumps(msg))
                    array = loads(await  ws.receive_bytes())
                    elapsed_time = time.time() - start_time
                    df.loc[len(df.index)] = [elapsed_time, size,iteration ]
            df.to_csv("aiohttp_np1d.csv")   
            df = pd.DataFrame([],columns=["elapsed_time","size","iteration_n"])


            for size in range(0,188317,413):
                msg = {}
                msg['key'] = np.random.random((size, 1)).tolist()

                for iteration in range(32): 
                    start_time = time.time()
                    await ws.send_json(json.dumps(msg))
                    array = json.loads(await  ws.receive_json())
                    elapsed_time = time.time() - start_time
                    df.loc[len(df.index)] = [elapsed_time, size,iteration]
            df.to_csv("aiohttp_json1d.csv")
            
            df = pd.DataFrame([],columns=["elapsed_time","size","iteration_n"])

            for size in range(0,455):
                msg = {}
                msg['key'] = np.random.random((size, size)).tolist()

                for iteration in range(32): 
                    start_time = time.time()
                    await ws.send_json(json.dumps(msg))
                    array = json.loads( await  ws.receive_json())
                    elapsed_time = time.time() - start_time
                    df.loc[len(df.index)] = [elapsed_time,size,iteration]

            df.to_csv("aiohttp_json2d.csv")
    
             
asyncio.get_event_loop().run_until_complete(benchmark())
