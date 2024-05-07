from discord.ext import commands
import discord
from database.conn import connection
from dotenv import load_dotenv
import os
from typing import Final


WELCOME_CHANNEL_ID: Final[int] = os.getenv("WELCOME_CHANNEL_ID")


class GreetCod(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot
        self.connection = connection


    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = member.guild
        guild_name = guild.name
        # sending welcome message to welocome channel
        welcome_channel = self.bot.get_channel(int(WELCOME_CHANNEL_ID))
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


async def setup(bot: commands.Bot):
    await bot.add_cog(GreetCod(bot))
