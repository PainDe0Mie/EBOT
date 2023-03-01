import discord
from .database.__init__ import GET, INSERT, REMOVE
from discord import app_commands
from discord.ext import commands

class WHITELIST(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Gérer la whitelist.")
    @app_commands.choices(action=[
        app_commands.Choice(name='ajouter', value=1),
        app_commands.Choice(name='retirer', value=2),
        app_commands.Choice(name='afficher', value=3),
    ])
    async def whitelist(self, interaction: discord.Interaction, action: app_commands.Choice[int], member: discord.User=None):
        if not interaction.user.id == 956183732841250946 and not interaction.user == interaction.guild.owner:
            return await interaction.response.send_message(f"❌ Seul le propriétaire du serveur peu {action.name} {'un membre' if action.value == 1 or action.value == 2 else 'les membres'} dans la whitelist !", ephemeral=True)
            
        await interaction.response.defer()
        user_get = GET(interaction.guild.id, "whitelist", "user_id")
        if action.value == 1 and not member == None:
            if not str(member.id) in user_get:
                INSERT(interaction.guild.id, "whitelist", "user_id", member.id)
                embed = discord.Embed(description=f"<:certif:1071159767822770208> {member.mention} a été whitelist avec succès !", color=discord.Color.green())
                embed.set_author(name="Ajout d'un membre dans la whitelist", icon_url=member.avatar.url)
                await interaction.followup.send(embed=embed)
            else:
                embed = discord.Embed(description=f":x: {member.mention} fait déjà parti de la whitelist !", color=discord.Color.red())
                embed.set_author(name="Ajout d'un membre dans la whitelist", icon_url=member.avatar.url)
                await interaction.followup.send(embed=embed)
        elif action.value == 2 and not member == None:
            if str(member.id) in user_get:
                REMOVE("whitelist", member.id)
                embed = discord.Embed(description=f"<:certif:1071159767822770208> {member.mention} a été enlever de la whitelist avec succès !", color=discord.Color.green())
                embed.set_author(name="Retirer un membre de la whitelist", icon_url=member.avatar.url)
                await interaction.followup.send(embed=embed)
            else:
                embed = discord.Embed(description=f":x: {member.mention} ne fait pas parti de la whitelist !", color=discord.Color.red())
                embed.set_author(name="Retirer un membre de la whitelist", icon_url=member.avatar.url)
                await interaction.followup.send(embed=embed)
        elif action.value == 3:
            members_withlisted = ""
            for user_id in user_get:
                members_withlisted = members_withlisted + f"<@{user_id}> ({user_id})\n"
            if user_get == []:
                members_withlisted = "*Aucun membre whitelist.*"
            embed = discord.Embed(description=members_withlisted, color=discord.Color.blue())
            embed.set_author(name="Liste des membres whitelist", icon_url=interaction.user.avatar.url)
            await interaction.followup.send(embed=embed)
        else:
            return await interaction.followup.send("❌ Merci d'indiquer un membre !")

async def setup(bot):
    await bot.add_cog(WHITELIST(bot))