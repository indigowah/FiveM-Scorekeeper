import discord
from discord import app_commands
from discord.ext import commands

import bot

class Wars(commands.GroupCog, name="wars"):
    def __init__(self, bot: bot.client):
        self.bot = bot
        super().__init__()

    @app_commands.command(name="create", description="Create a new war between two gangs")
    @app_commands.describe(
        attacking_gang="The name of the gang that is attacking",
        attacking_score="The score of the attacking gang",
        defending_gang="The name of the gang that is defending",
        defending_score="The score of the defending gang"
    )
    async def create_war(self, interaction: discord.Interaction, attacking_gang: str, attacking_score : int, defending_gang: str, defending_score: int):
        try:
            attacker = self.bot.db.gang.get_by_name(attacking_gang)
            defender = self.bot.db.gang.get_by_name(defending_gang)
        except ValueError as e:
            await interaction.response.send_message(str(e), ephemeral=True)
            return
        try:
            duel = self.bot.db.duel.create(attacker, attacking_score, defender, defending_score)
        except ValueError as e:
            await interaction.response.send_message(str(e), ephemeral=True)
            return
        await interaction.response.send_message(f"War created between '{attacking_gang}' and '{defending_gang}'. War ID: {duel.id}", ephemeral=True)

    @app_commands.command(name="delete", description="Delete a war by its war_id")
    @app_commands.describe(war_id="The ID of the war to delete")
    async def delete_war(self, interaction: discord.Interaction, war_id: int):
        try:
            duel = self.bot.db.duel.get_by_id(war_id)
        except Exception:
            await interaction.response.send_message(f"No war found with ID {war_id}.", ephemeral=True)
            return
        self.bot.db.duel.delete(duel)
        await interaction.response.send_message(f"War with ID {war_id} deleted.", ephemeral=True)

async def setup(bot: bot.client):
    await bot.add_cog(Wars(bot))
