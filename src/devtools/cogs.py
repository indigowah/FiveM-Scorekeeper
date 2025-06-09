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

    @command_group.command(name="batch_reload", description="Reload multiple cogs (comma-separated)")
    async def batch_reload(self, interaction: discord.Interaction, extensions: str):
        cogs = [e.strip() for e in extensions.split(",") if e.strip()]
        try:
            await self.bot.batch_cog_reload(cogs)
            await interaction.response.send_message(f"Batch reloaded: {', '.join(f'`{c}`' for c in cogs)}.")
        except Exception as e:
            await interaction.response.send_message(f"Batch reload failed: {e}")

    @command_group.command(name="batch_load", description="Load multiple cogs (comma-separated)")
    async def batch_load(self, interaction: discord.Interaction, extensions: str):
        cogs = [e.strip() for e in extensions.split(",") if e.strip()]
        try:
            await self.bot.batch_cog_enable(cogs)
            await interaction.response.send_message(f"Batch loaded: {', '.join(f'`{c}`' for c in cogs)}.")
        except Exception as e:
            await interaction.response.send_message(f"Batch load failed: {e}")

    @command_group.command(name="batch_unload", description="Unload multiple cogs (comma-separated)")
    async def batch_unload(self, interaction: discord.Interaction, extensions: str):
        cogs = [e.strip() for e in extensions.split(",") if e.strip()]
        try:
            await self.bot.batch_cog_disable(cogs)
            await interaction.response.send_message(f"Batch unloaded: {', '.join(f'`{c}`' for c in cogs)}.")
        except Exception as e:
            await interaction.response.send_message(f"Batch unload failed: {e}")

async def setup(bot : client):
    await bot.add_cog(CogManager(bot))