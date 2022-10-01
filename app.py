import asyncio
import os
from dbcontroller import create_db, DB_DIR, ScoreController
from listener import Listener

async def main():
    scorer = ScoreController()
    await scorer.startup()
    print("connected to db")

    print("starting tcp server...")
    listener = Listener()
    await listener.startup()
    print(f"tcp server listening on port {listener.port}")

    await listener.server.serve_forever()

    print("main done")
        
    


if __name__ == "__main__":
    if DB_DIR not in os.listdir("./"):
        create_db()

    try:
        asyncio.new_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        pass
