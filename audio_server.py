import asyncio
import os
import wave
from dbcontroller import ScoreController

AUDIO_PORT = 5000
AUDIO_DUMP_DIR = ".audio"
DISCORD_ID_STR_LEN = 18

class AudioServer:
    def __init__(self, scorer: ScoreController, port=AUDIO_PORT):
        self.scorer = scorer
        self.port = port

        try:
            os.rmdir(AUDIO_DUMP_DIR)
        except FileNotFoundError:
            pass

        os.mkdir(AUDIO_DUMP_DIR)

    async def startup(self):
        self.server = await asyncio.start_server(self.connection_callback, host="", port=self.port)

    async def read_discord_id(self, data) -> str:
        return data.decode("ascii")

    async def read_wav_data(self, discord_id, data):
        audio = wave.open(f"{AUDIO_DUMP_DIR}/{discord_id}.wav", "wb")
        audio.setframerate(44100)
        audio.setsampwidth(2)
        audio.setnchannels(1)

        for i in range(length * 1000):
            bits_data = await reader.read(length)
            audio.writeframes(data=bits_data)

        audio.close()

        await writer.drain()
        writer.close()

    async def connection_callback(self, reader, writer):
        print(f"audio connection!")
        discord_id = await self.read_discord_id(await reader.read(DISCORD_ID_STR_LEN * 8))

        length_data = await reader.read(4)
        length = int.from_bytes(length_data, "big")
        wav_data = await self.read_wav_data(discord_id, await reader.read(length))

