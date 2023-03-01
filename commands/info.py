import discord, psutil
from discord import app_commands
from discord.ext import commands

class INFO(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Informations diverses.")
    async def info(self, interaction: discord.Interaction):
        ram = psutil.virtual_memory().percent
        cpu = psutil.cpu_percent(interval=None)
        embed = discord.Embed(description=f"<:team:1071168815829889116> **Equipe d'EBOT:**\n> <:couronne:1071169019576598579>  Developpeur principal: ``PainDe0Mie#4811``\n\n<:epingler:1071162637326499840> **Partenaires fidèles:**\n> [Elexyr22 👑#0022](https://discord.gg/elexyr22)\n> ! iTaplock™#1212 // *Merci pour le logo !*\n\n<:mention:1071164688819294239> **Autres informations:**\n> CPU: {cpu}/<:infinity:1071168135840935987>%\n> RAM: {ram}/<:infinity:1071168135840935987>%")
        embed.set_author(name="EBOT - Credit & Information diverses", icon_url=self.bot.user.avatar.url)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(INFO(bot))