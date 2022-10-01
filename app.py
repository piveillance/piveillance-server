import asyncio
import os
from dbcontroller import create_db, DB_DIR, ScoreController


async def main():
    scorer = ScoreController()

    await scorer.startup()
    print("startup done")
    
    print(await scorer.get_user_score(1))
    await scorer.set_user_score(1, 32)
    print(await scorer.get_user_score(1))
    


if __name__ == "__main__":
    
    if DB_DIR not in os.listdir("./"):
        create_db()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
