import asyncio
import os
from dbcontroller import create_db, DB_DIR, ScoreController
from listener import AudioServer
from button_server import ButtonServer

async def main():
    scorer = ScoreController()
    await scorer.startup()
    print("connected to db")

    print("starting audio tcp server...")
    audio_server = AudioServer()
    await audio_server.startup()
    print(f"audio tcp server listening on port {audio_server.port}")

    print("starting button tcp server...")
    button_server = ButtonServer()
    await button_server.startup()
    print(f"button tcp server listening on port {button_server.port}")

    await asyncio.gather(audio_server.server.serve_forever(), button_server.server.serve_forever())
    #await audio_server.server.serve_forever()

    print("main done")
        
    


if __name__ == "__main__":
    if DB_DIR not in os.listdir("./"):
        create_db()

    try:
        asyncio.new_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        pass
