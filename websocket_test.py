import asyncio, websockets

async def main():
    async with websockets.connect("ws://localhost:5001") as socket:
        await socket.send("2 194891863742742529")
        print(await socket.recv())
