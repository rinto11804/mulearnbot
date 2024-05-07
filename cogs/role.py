from discord import app_commands
from discord.ext import commands
import discord
from database.conn import connection

from select_view import RoleSelectView


class RoleCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()

    @app_commands.command(name="select-role", description="select from available roles")
    async def select_role(self, interaction: discord.Interaction):
        view = RoleSelectView(connection)
        await interaction.response.send_message(view=view, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(RoleCog(bot))
