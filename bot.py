from typing import Final
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN: Final[str] = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()

intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    await bot.load_extension("cogs.greet")
    await bot.load_extension("cogs.word")
    await bot.load_extension("cogs.role")
    await bot.tree.sync()


bot.run(token=TOKEN)
