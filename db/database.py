import aiosqlite

DB_PATH = "database/bot.db"


# Setup database

async def setup_database():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS prefixes (
                guild_id INTEGER PRIMARY KEY,
                prefix TEXT DEFAULT ','
            )
        """)
        await db.commit()


# Get prefix

async def get_prefix(guild_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT prefix FROM prefixes WHERE guild_id = ?",
            (guild_id,)
        ) as cursor:
            row = await cursor.fetchone()

            if row:
                return row[0]

            return ","


# Set prefix

async def set_prefix(guild_id: int, prefix: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO prefixes (guild_id, prefix)
            VALUES (?, ?)
            ON CONFLICT(guild_id)
            DO UPDATE SET prefix = excluded.prefix
        """, (guild_id, prefix))

        await db.commit()