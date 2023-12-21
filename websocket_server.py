import asyncio
import websockets


async def recieve_return(ws):
    async for msg in ws:
        await ws.send(msg)


async def main():
    async with websockets.serve(recieve_return, "localhost", 8764):
        await asyncio.Future()  # run forever

asyncio.run(main())
