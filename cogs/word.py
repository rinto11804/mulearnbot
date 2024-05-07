from discord.ext import commands
from discord import app_commands, Interaction, Message, Member
from database.conn import connection


class WordCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author == self.bot.user:
            return
        content = message.content
        user_id = message.author.id
        try:
            cursor = self.connection.cursor()
            for word in content.split():
                cursor.execute(
                    "INSERT INTO user_word(discord_id, word) VALUES (%s, %s)",
                    (str(user_id), word),
                )
            self.connection.commit()
        except Exception as e:
            print("failed to add user word")

    @app_commands.command(
        name="user-status",
        description="Gives the 10 most used words by the specified user.",
    )
    async def user_status(self, interaction: Interaction, user: Member):
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
                "Failed to load user status", ephemeral=True
            )

    @app_commands.command(
        name="word-status", description="Gives the 10 most used words."
    )
    async def word_status(self, interaction: Interaction):
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
            await interaction.response.send_message(
                "Failed to load word status", ephemeral=True
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(WordCog(bot))
