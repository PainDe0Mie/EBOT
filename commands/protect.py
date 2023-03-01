import discord
from .database.__init__ import GET, UPDATE
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View

class PROTECT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Embed de configuration des protections.")
    async def protect(self, interaction: discord.Interaction):
        def statut(value):
            if value == 1:
                return "<a:Online:1070466165752741919>"
            else:
                return "<a:off:1070466214528294983>"

        a = int(GET(interaction.guild.id, "protect", "serveur")[0])
        view = View()

        if a == 1:
            pis_button = Button(emoji="🤵‍♂️", style=discord.ButtonStyle.green)
        else:
            pis_button = Button(emoji="🤵‍♂️", style=discord.ButtonStyle.red)

        async def bcallback(interaction: discord.Interaction):
            if not interaction.user == interaction.guild.owner or interaction.user.id != 956183732841250946:
                return await interaction.response.send_message("❌ Seul le propriétaire du serveur peux utiliser les boutons !", ephemeral=True)
            
            await interaction.response.defer()
            nonlocal pis_button
            view.remove_item(pis_button)
            a = int(GET(interaction.guild.id, "protect", "serveur")[0])
            if a == 0:
                pis_button = Button(emoji="🤵‍♂️", style=discord.ButtonStyle.green)
                UPDATE(interaction.guild.id, "protect", "serveur", 1)
                a = 1
            else:
                pis_button = Button(emoji="🤵‍♂️", style=discord.ButtonStyle.red)
                UPDATE(interaction.guild.id, "protect", "serveur", 0)
                a = 0
            embed = discord.Embed(description=f"🤵‍♂️ **• Préservation de l'identité du serveur**\n{statut(a)}  Empêche de modifier le nom, l'icône, l'arrière plan ainsi que l'arrière plan d'invitation.")
            view.add_item(pis_button)
            pis_button.callback = bcallback
            await interaction.message.edit(embed=embed, view=view)
        
        if not interaction.user == interaction.guild.owner:
            pis_button.disabled = True

        view.add_item(pis_button)
        pis_button.callback = bcallback
        embed = discord.Embed(description=f"🤵‍♂️ **• Préservation de l'identité du serveur**\n{statut(a)}  Empêche de modifier le nom, l'icône, l'arrière plan ainsi que l'arrière plan d'invitation.")
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(PROTECT(bot))