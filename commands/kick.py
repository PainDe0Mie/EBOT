import discord
from discord import app_commands
from discord.ext import commands

class KICK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Kick un membre.")
    async def kick(self, interaction: discord.Interaction, membre: discord.Member, raison: str="Aucune raison donnée."):
        if not interaction.user.guild_permissions.kick_members:
            return await interaction.response.send_message("Vous n'avez pas la permission ``kick_members``.", ephemeral=True)

        try:
            await membre.kick(reason=raison)
            embed = discord.Embed(description=f"{membre.mention}** a bien été kick du serveur !**\n\n> Par: {interaction.user.mention}\n> Raison: {raison}")
            embed.set_author(name=self.bot.user.name + " - Kick:", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message("Il semblerait que je n'ai pas la permission ``kick_members``.")

async def setup(bot):
    await bot.add_cog(KICK(bot))