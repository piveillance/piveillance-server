import asyncio, wave


class AudioServer:
    def __init__(self, port: int = 8888):
        self.port = port

    async def listen(self):
        self.server = await asyncio.start_server(self.handle_connection, "127.0.0.1", self.port)
        print("listening!")

        async with self.server:
            await self.server.serve_forever()

    async def handle_connection(self, reader, writer):
        length_data = await reader.read(4)
        length = int.from_bytes(length_data, "big")
        audio = wave.open("/home/matthewl/output.wav", "wb")
        audio.setframerate(44100)
        audio.setsampwidth(2)
        audio.setnchannels(1)

        for i in range(length * 1000):
            bits_data = await reader.read(length*10)
            bits = bits_data
            audio.writeframes(data=bits)

        audio.close()

        await writer.drain()
        writer.close()


if __name__ == "__main__":
    server = AudioServer()
    asyncio.run(server.listen())
