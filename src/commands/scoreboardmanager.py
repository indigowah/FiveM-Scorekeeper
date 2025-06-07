import discord
from discord.ext import commands
from discord import app_commands

from bot import client
import os
import json

class ScoreboardManager(commands.Cog):
    def __init__(self, bot : client):
        self.bot = bot

    scoreboard = app_commands.Group(name="scoreboard", description="Scoreboard management commands")

    @scoreboard.command(name="setup", description="Setup a scoreboard in a specific channel")
    @app_commands.describe(channel="The channel to setup the scoreboard in")
    async def setup(self, interaction: discord.Interaction, channel: discord.TextChannel):
        embed = discord.Embed(
            title="Scoreboard",
            description="A new scoreboard has been set up!",
            color=discord.Color.blue()
        )
        # Get the path to the directory containing main
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(base_dir, "configuration.json")
        
        self.bot.logger.info(f"Setting up scoreboard in {channel.name} with config path {config_path}")

        # Send the embed and get the message object
        message = await channel.send(embed=embed)

        # Store the message_id in the configuration file
        config = {}
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config = json.load(f)

        config["scoreboard_message_id"] = message.id

        self.bot.logger.info(f"Scoreboard message ID set to {message.id} in configuration.")

        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)
            
        await interaction.response.send_message(f"Scoreboard set up in {channel.mention}.", ephemeral=True)

    @scoreboard.command(name="addscore", description="Add the score of a duel to the scoreboard")
    @app_commands.describe(
        attacking_gang="The attacking gang",
        attacking_gang_score="The score of the attacking gang",
        defending_gang="The defending gang",
        defending_gang_score="The score of the defending gang"
    )
    async def addscore(self, interaction: discord.Interaction, 
                       attacking_gang : str, attacking_gang_score: int, 
                       defending_gang: str, defending_gang_score: int):
        # Get the path to the directory containing main
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(base_dir, "configuration.json")
        
        # Load the configuration file
        config = {}
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config = json.load(f)
        else:
            self.bot.logger.error("Configuration file not found. Please set up the scoreboard first.")
            await interaction.response.send_message("Configuration file not found. Please set up the scoreboard first.", ephemeral=True)
            return
        message_id = config.get("scoreboard_message_id")
        if not message_id:
            self.bot.logger.error("Scoreboard message ID not found in configuration.")
            await interaction.response.send_message("Scoreboard message ID not found in configuration. Please set up the scoreboard first.", ephemeral=True)
            return
        # Fetch the channel and message
        channel = self.bot.get_channel(interaction.channel_id) # type: ignore
        if not channel:
            self.bot.logger.error("Channel not found.")
            await interaction.response.send_message("Channel not found.", ephemeral=True)
            return
        try:
            message = await channel.fetch_message(message_id) # type: ignore
        except discord.NotFound:
            self.bot.logger.error("Scoreboard message not found.")
            await interaction.response.send_message("Scoreboard message not found. Please set up the scoreboard first.", ephemeral=True)
            return
        except discord.Forbidden:
            self.bot.logger.error("Bot does not have permission to fetch the scoreboard message.")
            await interaction.response.send_message("Bot does not have permission to fetch the scoreboard message.", ephemeral=True)
            return
        except discord.HTTPException as e:
            self.bot.logger.error(f"Failed to fetch scoreboard message: {e}")
            await interaction.response.send_message("Failed to fetch scoreboard message. Please try again later.", ephemeral=True)
            return
        
        # Read the current embed
        embed = message.embeds[0] if message.embeds else discord.Embed(title="Scoreboard", description="Current scores", color=discord.Color.blue()) # type: ignore
        # Update the embed with the new scores
        embed.description = (embed.description or "") + f"\n**{attacking_gang}**: {attacking_gang_score} - {defending_gang_score} :{defending_gang}" # type: ignore
        # Edit the message with the updated embed
        await message.edit(embed=embed) # type: ignore
        self.bot.logger.info(f"Added score for {attacking_gang} vs {defending_gang} to the scoreboard.")
        await interaction.response.send_message(f"Added score for {attacking_gang} vs {defending_gang} to the scoreboard.", ephemeral=True)

async def setup(bot : client):
    await bot.add_cog(ScoreboardManager(bot))