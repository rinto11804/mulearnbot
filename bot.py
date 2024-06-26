from typing import Final
import discord
from discord.ext import commands
from dotenv import load_dotenv
import psycopg2
import os
from select_view import RoleSelectView


load_dotenv()

TOKEN: Final[str] = os.getenv("BOT_TOKEN")
WELCOME_CHANNEL_ID: Final[int] = os.getenv("WELCOME_CHANNEL_ID")
DB_URL: Final[str] = os.getenv("DB_URL")

try:
    connection = psycopg2.connect(dsn=DB_URL + "=disable")
except Exception as e:
    print(e)

intents = discord.Intents.default()

intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)


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
        print("failed to add user word")


@bot.tree.command(name="word-status", description="Gives the 10 most used words.")
async def word_status(interaction: discord.Interaction):
    try:
        cursor = connection.cursor()
        cursor.execute(
            """SELECT word, count(*) AS count
                FROM (
                SELECT lower(word) AS word
                FROM user_word
                ) AS word_counts
                GROUP BY word
                ORDER BY count DESC
                LIMIT 10;"""
        )
        rows = cursor.fetchall()
        connection.commit()
        res = "\n".join([f"{row[0]}: {row[1]}" for row in rows])
        await interaction.response.send_message(res, ephemeral=True)
    except Exception as e:
        print("Failed to load word status")
        await interaction.response.send_message("Failed to load word status",ephemeral=True)


@bot.tree.command(
    name="user-status",
    description="Gives the 10 most used words by the specified user.",
)
async def word_status(interaction: discord.Interaction, user: discord.Member):
    try:
        cursor = connection.cursor()
        cursor.execute(
            """SELECT word, count(*) AS count
                FROM (
                SELECT lower(word) AS word
                FROM user_word WHERE discord_id = '%s'
                ) AS word_counts
                GROUP BY word
                ORDER BY count DESC
                LIMIT 10;""",
            (user.id,),
        )
        rows = cursor.fetchall()
        connection.commit()
        res = "\n".join([f"{row[0]}: {row[1]}" for row in rows])
        await interaction.response.send_message(res, ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(
            "Failed to load use status", ephemeral=True
        )


@bot.tree.command(name="select-role", description="select from available roles")
async def select_role(interaction: discord.Interaction):
    view = RoleSelectView(connection)
    await interaction.response.send_message(view=view,ephemeral=True)


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

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.HTTPException) and error.status == 429:
        await ctx.send("Woah there! I'm being ratelimited. Please try again in a few seconds.")
    else:
        await ctx.send("An error occured. Please try again in a few seconds.")
        print(f"An error occurred: {error}")

@bot.event
async def on_ready():
    await bot.tree.sync()


bot.run(token=TOKEN)
