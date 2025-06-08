import discord
from discord import app_commands
from discord.ext import commands

import bot

class Gangs(commands.GroupCog, name="gangs"):
    def __init__(self, bot: bot.client):
        self.bot = bot
        super().__init__()

    @app_commands.command(name="create", description="Create a new gang")
    async def create_gang(self, interaction: discord.Interaction, name: str):
        self.bot.db.gang.create(name)
        await interaction.response.send_message(f"Gang '{name}' created.", ephemeral=True)

    @app_commands.command(name="delete", description="Delete an existing gang")
    async def delete_gang(self, interaction: discord.Interaction, name: str):
        try:
            gang = self.bot.db.gang.get_by_name(name)
        except ValueError as e:
            await interaction.response.send_message(str(e), ephemeral=True)
            return
        self.bot.db.gang.delete(gang)
        await interaction.response.send_message(f"Gang '{name}' deleted.", ephemeral=True)

    @app_commands.command(name="edit", description="Edit an existing gang's name")
    async def edit_gang(self, interaction: discord.Interaction, old_name: str, new_name: str):
        try:
            gang = self.bot.db.gang.get_by_name(old_name)
        except ValueError as e:
            await interaction.response.send_message(str(e), ephemeral=True)
            return
        try:
            self.bot.db.gang.update_name(gang, new_name)
        except ValueError as e:
            await interaction.response.send_message(str(e), ephemeral=True)
            return
        await interaction.response.send_message(f"Gang '{old_name}' renamed to '{new_name}'.", ephemeral=True)

async def setup(bot: bot.client):
    await bot.add_cog(Gangs(bot))