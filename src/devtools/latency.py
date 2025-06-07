import discord
from discord.ext import commands

from bot import client

class LatencyCog(commands.Cog):
    def __init__(self, bot : client):
        self.bot = bot

    @discord.app_commands.command(name="latency", description="Responds with the bot's latency.")
    async def latency(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)  # Convert to milliseconds
        await interaction.response.send_message(f"Latency: {latency}ms")
        self.bot.logger.info(f"Latency: {latency}ms")

async def setup(bot : client):
    await bot.add_cog(LatencyCog(bot))