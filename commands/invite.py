import discord
from discord import app_commands
from discord.ext import commands

class INVITE(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Invitation du bot.")
    @commands.has_permissions(manage_messages=True)
    async def invite(self, interaction: discord.Interaction):
        await interaction.response.defer()
        embed = discord.Embed(description="> **Invite moi** en cliquant juste [ici](https://discord.com/oauth2/authorize?client_id=965385515618676746&permissions=1644971949559&scope=bot) !\n> Si tu as des questions, n'hésite pas à **rejoindre** le [serveur support](https://discord.gg/q42m4fRhu2) !", color=discord.Color.blue())
        await interaction.followup.send(embed=embed)
        
async def setup(bot):
    await bot.add_cog(INVITE(bot))