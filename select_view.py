from discord.ui import View, RoleSelect
import discord
import psycopg


class RoleSelectView(View):
    def __init__(self, conn: psycopg.connection.Connection):
        super().__init__()
        self.conn = conn

    @discord.ui.select(cls=RoleSelect)
    async def select_callback(
        self, interaction: discord.Interaction, select: RoleSelect
    ):
        role_name = select.values[0].name
        user_id = interaction.user.id
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT role FROM user_role WHERE discord_id = '%s';", (user_id,)
        )
        rows = cursor.fetchall()
        self.conn.commit()

        if len(rows) == 0:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO user_role(discord_id, role) VALUES ('%s', %s);",
                (user_id, role_name),
            )
            self.conn.commit()
        elif rows[0][0] == role_name:
            await interaction.response.send_message(
                f"Role:{role_name} is already assigned to you"
            )
            return
        else:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE user_role SET role=%s WHERE discord_id = '%s';",
                (role_name, user_id),
            )
            self.conn.commit()
        await interaction.user.add_roles(
            discord.utils.get(interaction.user.guild.roles, name=role_name)
        )
        await interaction.response.send_message(f"Role:{role_name} is assigned to you")
