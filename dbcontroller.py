import aiosqlite
import sqlite3
import os
from typing import Optional

DB_DIR = "db"
DB_FILE = "scores.db"
DB_PATH = DB_DIR + "/" + DB_FILE

def create_db():
    os.mkdir(DB_DIR)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE Scores (
        UserID int,
        Score int
        )""")
    conn.commit()
    print("db created")
    conn.close()


class ScoreController:
    
    async def startup(self):
        self.db = await aiosqlite.connect(DB_PATH)

    """
    Gets a user's score, or None if the user does not exist.
    """
    async def get_user_score(self, discord_id: int) -> Optional[int]:
        async with self.db.cursor() as c:
            await c.execute("SELECT Score FROM Scores WHERE UserID=?;", [discord_id])
            result = await c.fetchone()
            return None if result is None else result[0]

    """
    Sets a user's score, updating or adding entries where appropriate. 
    """
    async def set_user_score(self, discord_id: int, score: int):
        async with self.db.cursor() as c:
            if (await self.get_user_score(discord_id)) is None:
                await c.execute("INSERT INTO Scores VALUES (?, ?);", [discord_id, score])
            else:
                await c.execute("UPDATE Scores SET Score=? WHERE UserID=?;", [score, discord_id])

