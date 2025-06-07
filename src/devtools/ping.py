import discord
from discord.ext import commands

from bot import client

class PingCog(commands.Cog):
    def __init__(self, bot : client):
        self.bot = bot

    @discord.app_commands.command(name="ping", description="Responds with pong.")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("pong")
        self.bot.logger.info("Ping Pong!")

async def setup(bot : client):
    await bot.add_cog(PingCog(bot))