from typing import Final
import discord
from discord.ext import commands
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

    # sending welcome message to welocome channel
    welcome_channel = client.get_channel(int(WELCOME_CHANNEL_ID))
    if welcome_channel is not None:
        to_send = f"Welcome {member._user.name} to {guild.name}!"
        try:
            await welcome_channel.send(to_send,mention_author=True)
        except Exception as e:
            print(e)
    
    # sending welcome message to users inbox
    try:
        await member.send(to_send,mention_author=True)
    except Exception as e:
        print(e)


client.run(token=TOKEN)
