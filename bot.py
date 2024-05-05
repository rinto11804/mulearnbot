from typing import Final
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import psycopg2


load_dotenv()


TOKEN: Final[str] = os.getenv("BOT_TOKEN")
WELCOME_CHANNEL_ID: Final[int] = os.getenv("WELCOME_CHANNEL_ID")
DB_URL: Final[str] = os.getenv("DB_URL")

try:
    connection = psycopg2.connect(dsn=DB_URL)
except Exception as e:
    print(e)

intents = discord.Intents.default()

intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user} ID: {bot.user.id}")


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    content = message.content
    user_id = message.author.id
    try:
        cursor = connection.cursor()
        for word in content.split():
            cursor.execute(
                "INSERT INTO user_word(discord_id, word) VALUES (%s, %s)",
                (str(user_id), word),
            )
        connection.commit()
    except Exception as e:
        print(e)


@bot.event
async def on_member_join(member: discord.Member):
    guild = member.guild
    guild_name = guild.name
    # sending welcome message to welocome channel
    welcome_channel = bot.get_channel(int(WELCOME_CHANNEL_ID))
    if welcome_channel:
        try:
            await welcome_channel.send(
                f"Welcome {member.mention} to server!", mention_author=True
            )
        except Exception as e:
            print(e)

    # sending welcome message to users inbox
    try:
        await member.send(
            f"Welcome {member.mention} to {guild_name}!", mention_author=True
        )
    except Exception as e:
        print(e)


bot.run(token=TOKEN)
