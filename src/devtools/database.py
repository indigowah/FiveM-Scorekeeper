import discord
from discord import app_commands
from discord.ext import commands
import bot
import random

class DatabaseTools(commands.GroupCog, name="database"):
    def __init__(self, bot: bot.client):
        self.bot = bot
        super().__init__()

    @app_commands.command(name="flush", description="Flush (delete) all data from the database.")
    async def flush_database(self, interaction: discord.Interaction):
        try:
            # Delete all duels first (due to FK constraints), then all gangs
            for duel in self.bot.db.duel.get_all():
                self.bot.db.duel.delete(duel)
            for gang in self.bot.db.gang.get_all():
                self.bot.db.gang.delete(gang)
            await interaction.response.send_message("Database flushed (all gangs and duels deleted).", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Error flushing database: {e}", ephemeral=True)

    @app_commands.command(name="fake_data", description="Populate the database with fake gangs and duels.")
    async def fake_data(self, interaction: discord.Interaction):
        try:
            # Add fake gangs
            gang_names = [f"Gang_{i}" for i in range(1, 7)]
            gangs = []
            for name in gang_names:
                try:
                    gang = self.bot.db.gang.create(name)
                except ValueError:
                    gang = self.bot.db.gang.get_by_name(name)
                gangs.append(gang)
            # Add fake duels
            for _ in range(8):
                g1, g2 = random.sample(gangs, 2)
                score1 = random.randint(0, 10)
                score2 = random.randint(0, 10)
                try:
                    self.bot.db.duel.create(g1, score1, g2, score2)
                except Exception:
                    continue
            await interaction.response.send_message("Fake data added: 6 gangs, 8 duels.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Error adding fake data: {e}", ephemeral=True)

async def setup(bot: bot.client):
    await bot.add_cog(DatabaseTools(bot))
