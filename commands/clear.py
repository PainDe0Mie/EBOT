import discord
from discord import app_commands
from discord.ext import commands

class CLEAR(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Efface les messages.")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, nombres: int, channel: discord.TextChannel):
        if interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(f"🗑️ J'ai effacer ``{nombres}`` messages dans {channel.mention} avec succès !")
            await channel.purge(limit=nombres)
        else:
            await interaction.response.send_message(f"❌ Vous n'avez pas la permission de gérer les messages !")

async def setup(bot):
    await bot.add_cog(CLEAR(bot))