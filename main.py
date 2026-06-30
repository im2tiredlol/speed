import os
import asyncio
import discord
from discord.ext import commands

from database.database import get_prefix, setup_database

# Bot config

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True


# Prefix handler

async def prefix_handler(bot, message):
    if not message.guild:
        return ","

    return await get_prefix(message.guild.id)


bot = commands.Bot(
    command_prefix=prefix_handler,
    intents=intents,
    help_command=None
)

# Global embed colors

DEFAULT_COLOR = discord.Color.from_str("#323336")
OK_COLOR = discord.Color.from_str("#A4EB78")
WARN_COLOR = discord.Color.from_str("#FAA81A")
ERROR_COLOR = discord.Color.from_str("#FF6464")


# Events

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")


# Load cogs

async def load_cogs():
    path = "commands/moderation"

    for file in os.listdir(path):
        if file.endswith(".py") and not file.startswith("_"):
            await bot.load_extension(f"commands.moderation.{file[:-3]}")


# Start bot

async def main():
    await setup_database()

    async with bot:
        await load_cogs()
        await bot.start("YOUR_TOKEN_HERE")


if __name__ == "__main__":
    asyncio.run(main())