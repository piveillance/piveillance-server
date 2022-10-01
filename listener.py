import asyncio
import wave

TCP_PORT = 5000
AUDIO_DUMP_DIR = ".audio"
DISCORD_ID_STR_LEN = 18

class Listener:
    def __init__(self, port=TCP_PORT):
        self.port = port

    async def startup(self):
        self.server = await asyncio.start_server(self.connection_callback, host="", port=self.port)

    async def read_discord_id(self, data) -> str:
        return data.decode("ascii")

    async def read_wav_data(self, data):
        bits = int.from_bytes(data, "big")
        audio = wave.open(f"{}.wav", "w")
        audio.setframerate(44100)
        audio.setsampwidth(2)
        audio.setnchannels(1)
        audio.writeframes()
        audio.close()

        await writer.drain()
        writer.close()

    async def connection_callback(self, reader, writer):
        print(f"connection established")
        discord_id = await self.read_discord_id(await reader.read(DISCORD_ID_STR_LEN * 8))

        length_data = await reader.read(4)
        length = int.from_bytes(length_data, "big")
        wav_data = await self.read_wav_data(await reader.read(length))

