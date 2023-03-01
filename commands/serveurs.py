import discord
from discord import app_commands
from discord.ext import commands

class SERVEURS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Nombre de serveur du bots.")
    async def serveurs(self, interaction: discord.Interaction):
        embed = discord.Embed(description=f"Je suis sur **{len(self.bot.guilds)} serveurs**, merci !! <a:panda_woooo:1041449209955618898>", color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(SERVEURS(bot))