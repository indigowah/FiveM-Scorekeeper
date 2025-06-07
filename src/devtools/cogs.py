import discord
from discord import app_commands
from discord.ext import commands

from bot import client

class CogManager(commands.Cog, name="Cog Manager"):
    def __init__(self, bot : client):
        self.bot = bot

    command_group = app_commands.Group(name="cog", description="Manage bot cogs")

    @command_group.command(name="load", description="Load a cog")
    async def load(self, interaction: discord.Interaction, extension: str):
        try:
            await self.bot.cog_enable(extension)
            await interaction.response.send_message(f"Loaded `{extension}`.")
        except Exception as e:
            await interaction.response.send_message(f"Failed to load `{extension}`: {e}")

    @command_group.command(name="unload", description="Unload a cog")
    async def unload(self, interaction: discord.Interaction, extension: str):
        try:
            await self.bot.cog_disable(extension)
            await interaction.response.send_message(f"Unloaded `{extension}`.")
        except Exception as e:
            await interaction.response.send_message(f"Failed to unload `{extension}`: {e}")

    @command_group.command(name="reload", description="Reload a cog")
    async def reload(self, interaction: discord.Interaction, extension: str):
        try:
            await self.bot.cog_reload(extension)
            await interaction.response.send_message(f"Reloaded `{extension}`.")
        except Exception as e:
            await interaction.response.send_message(f"Failed to reload `{extension}`: {e}")

async def setup(bot : client):
    await bot.add_cog(CogManager(bot))