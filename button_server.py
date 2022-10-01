import asyncio
from dbcontroller import ScoreController
import websockets

BUTTON_PORT = 5001
#DISCORD_ID_STR_LEN = 18

button_scores = [300, -300, 150, -150, 80, -80, 20, -20]

class ButtonServer:
    def __init__(self, scorer: ScoreController, port=BUTTON_PORT):
        self.scorer = scorer
        self.port = port

    async def startup(self):
        #self.server = await asyncio.start_server(self.connection_callback, host="", port=self.port)#
        await websockets.serve(self.handler, "", BUTTON_PORT)

    async def handler(ws, path):
        data: str = await ws.recv()
        print(f" recv: {data}")
        discord_id, button_id = data.split(" ")

        # in case user doesn't exist...
        if (await self.scorer.get_user_score(discord_id)) is None:
            await self.scorer.set_user_score(discord_id, 800)
        
        orig_score = self.scorer.get_user_score(discord_id)
        score = orig_score + button_scores[int(button_id)]
        score = 0 if score < 0 else (1000 if score > 1000 else score)
        self.scorer.set_user_score(discord_id, score)

        await ws.send(f"{discord_id} {score}")

    #async def read_discord_id(self, data) -> str:
    #    return data.decode("ascii")

    #async def read_score_change(self, data) -> int:
    #    return int.from_bytes(data, "big")

    """
    async def connection_callback(self, reader, writer):
        print("button connection!")
        discord_id = await self.read_discord_id(await reader.read(DISCORD_ID_STR_LEN * 8))
        
        alive = True
        while alive:
            score_change = await self.read_score_change(await reader.read(1))

        orig_score = self.scorer.get_user_score(discord_id)
        score = orig_score + score_change
        score = 0 if score < 0 else (1000 if score > 1000 else score)
        self.scorer.set_user_score(discord_id, score)

        writer.write(score.to_bytes(2, "big"))"""

