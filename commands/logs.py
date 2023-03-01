import discord
from .database.__init__ import ELOGS, SETUP
from discord import app_commands
from discord.ext import commands

class LOGS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Definir ou changer les logs.")
    async def logs(self, interaction: discord.Interaction, channel: discord.TextChannel):
        if not interaction.user == interaction.guild.owner or interaction.user.id != 956183732841250946:
            return await interaction.response.send_message(f"❌ Seul le propriétaire du serveur peux définir les logs !", ephemeral=True)
        await interaction.response.defer()
        try:
            SETUP(guild_id=interaction.guild.id)
        except:
            pass
        logs = ELOGS(guild_id=interaction.guild.id, logs_id=channel.id)
        if logs == "success":
            await interaction.followup.send(f"<:certif:1071159767822770208> Les logs ont bien été défini sur {channel.mention} !")

async def setup(bot):
    await bot.add_cog(LOGS(bot))