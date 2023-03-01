import discord
from discord import app_commands
from discord.ext import commands

class UNBAN(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Débannir un membre.")
    async def unban(self, interaction: discord.Interaction, membre: discord.User, raison: str="Aucune raison donnée."):
        if not interaction.user.guild_permissions.ban_members:
            return await interaction.response.send_message("Vous n'avez pas la permission ``ban_members``.", ephemeral=True)

        try:
            await interaction.guild.unban(membre, reason=raison)
            embed = discord.Embed(description=f"{membre.mention}** a bien été débanni du serveur !**\n\n> Par: {interaction.user.mention}\n> Raison: {raison}")
            embed.set_author(name=self.bot.user.name + " - Unban:", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message("Il semblerait que je n'ai pas la permission ``ban_members``.")

async def setup(bot):
    await bot.add_cog(UNBAN(bot))