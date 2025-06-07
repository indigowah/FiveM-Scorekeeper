import discord
from discord.ext import commands
from discord import app_commands

from bot import client

class ScoreboardManager(commands.Cog):
    def __init__(self, bot : client):
        self.bot = bot

    scoreboard = app_commands.Group(name="scoreboard", description="Scoreboard management commands")

    @scoreboard.command(name="spawn", description="Spawn a scoreboard in a specific channel")
    @app_commands.describe(channel="The channel to spawn the scoreboard in")
    async def spawn(self, interaction: discord.Interaction, channel: discord.TextChannel):
        embed = discord.Embed(
            title="Scoreboard",
            description="A new scoreboard has been spawned!",
            color=discord.Color.blue()
        )
        await channel.send(embed=embed)
        await interaction.response.send_message(f"Scoreboard spawned in {channel.mention}.", ephemeral=True)

async def setup(bot : client):
    await bot.add_cog(ScoreboardManager(bot))