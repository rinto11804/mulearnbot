from typing import Final
import discord
import os
from dotenv import load_dotenv


load_dotenv()

TOKEN: Final[str] = os.getenv("BOT_TOKEN")
WELCOME_CHANNEL_ID: Final[int] = os.getenv("WELCOME_CHANNEL_ID")


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user} ID: {client.user.id}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.reply("Hello!", mention_author=True)


@client.event
async def on_member_join(member: discord.Member):
    guild = member.guild
    welcome_channel = client.get_channel(WELCOME_CHANNEL_ID)
    if welcome_channel is not None:
        to_send = f"Welcome {member.mention} to {guild.name}!"
        await welcome_channel.send(to_send)


client.run(token=TOKEN)
