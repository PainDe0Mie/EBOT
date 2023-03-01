import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View, Select

class HELP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Affiche toute les commandes du bot.")
    async def help(self, interaction: discord.Interaction):
        A = discord.Embed(description=f"**Salut {interaction.user.name}, moi c'est EBOT ! Je suis en __slash commande__** ``/`` **!**\n\n<a:Tempo:1070465439471239189> EBOT est en maintenance !\n\n> Suggérer une commande: ``/suggestion``\n> *Dernière MAJ: 22/02/2023*", color=discord.Color.blue())
        A.set_footer(text=f"Demandé par {interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar.url)
        A.set_author(name="EBOT - Besoin d'aide ?", icon_url=self.bot.user.avatar.url)

        B = discord.Embed(description=f":jigsaw: **Autres commandes:**\n> ``/ping`` · Affichier la latence du bot.\n> ``/serveurs`` · Afficher le nombre de serveurs sur lesquels je suis présent.\n> ``/invite`` · Invitation du bot & support.\n> ``/info`` · Informations diverses.\n> ``/bug`` · Rapporter un dysfonctionnement d'une commande.", color=discord.Color.blue())
        B.set_footer(text=f"Demandé par {interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar.url)
        B.set_author(name="EBOT - Besoin d'aide ?", icon_url=self.bot.user.avatar.url)

        C = discord.Embed(description=f"⚙️ **Gestion du serveur:**\n> ``/add_emoji`` · Ajouter un emoji sur votre serveur.\n> ``/del_emoji`` · Supprimer un emoji de votre serveur.", color=discord.Color.blue())
        C.set_footer(text=f"Demandé par {interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar.url)
        C.set_author(name="EBOT - Besoin d'aide ?", icon_url=self.bot.user.avatar.url)

        D = discord.Embed(description=f"🚔 **Modération du serveur:**\n> ``/protect`` · Embed des protections du serveur.\n> ``/whitelist`` · Gestion de la whitelist.\n> ``/logs`` · Definir des logs.\n> ``/ban`` · Bannir un utilisateur du serveur.\n> ``/unban`` · Débannir un utilisateur du serveur.\n> ``/kick`` · Expulser un membre du serveur.", color=discord.Color.blue())
        D.set_footer(text=f"Demandé par {interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar.url)
        D.set_author(name="EBOT - Besoin d'aide ?", icon_url=self.bot.user.avatar.url)

        select = Select(options=[
            discord.SelectOption(label="Menu", emoji="🏡"),
            discord.SelectOption(label="Gestion du serveur", emoji="⚙️"),
            discord.SelectOption(label="Modération du serveur", emoji="🚔"),
            discord.SelectOption(label="Autres", emoji="🧩"),
        ])
        
        button1 = Button(label="Statut", emoji="<a:online:1038157228538081320>", url="https://status.watchbot.app/bot/965385515618676746")
        button2 = Button(label="Support", emoji="<:EBOT:1070072671934619698>", url="https://discord.gg/2kNa7RYWJp")
        button3 = Button(label="Github", emoji="<:github:1068640119055200338>", url="https://github.com/PainDe0Mie/EBOT/", disabled=True)
        
        view = View()
        view.add_item(select)
        view.add_item(button1)
        view.add_item(button2)
        view.add_item(button3)
        
        await interaction.response.send_message(embed=A, view=view)

        async def select_callback(interaction):
            if select.values[0] == "Menu":
                await interaction.response.defer()
                return await interaction.message.edit(embed=A)
            elif select.values[0] == "Autres":
                await interaction.response.defer()
                return await interaction.message.edit(embed=B)
            elif select.values[0] == "Gestion du serveur":
                await interaction.response.defer()
                return await interaction.message.edit(embed=C)
            elif select.values[0] == "Modération du serveur":
                await interaction.response.defer()
                return await interaction.message.edit(embed=D)

        select.callback = select_callback

async def setup(bot):
    await bot.add_cog(HELP(bot))