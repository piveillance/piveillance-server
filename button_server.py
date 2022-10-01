import asyncio
from dbcontroller import ScoreController

BUTTON_PORT = 5001
DISCORD_ID_STR_LEN = 18

class ButtonServer:
    def __init__(self, scorer: ScoreController, port=BUTTON_PORT):
        self.scorer = scorer
        self.port = port

    async def startup(self):
        self.server = await asyncio.start_server(self.connection_callback, host="", port=self.port)

    async def read_discord_id(self, data) -> str:
        return data.decode("ascii")

    async def read_score_change(self, data) -> int:
        return int.from_bytes(data, "big")

    async def connection_callback(self, reader, writer):
        print("button connection!")
        discord_id = await self.read_discord_id(await reader.read(DISCORD_ID_STR_LEN * 8))
        score_change = await self.read_score_change(await reader.read(1))

        orig_score = self.scorer.get_user_score(discord_id)
        score = orig_score + score_change
        score = 0 if score < 0 else (1000 if score > 1000 else score)
        self.scorer.set_user_score(discord_id, score)

        writer.write(score.to_bytes(2, "big"))
