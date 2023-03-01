import discord, os
from discord import app_commands
from discord.ext import commands

owner_id = 956183732841250946

class DELEMOJI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Supprimer un emoji sur votre serveur.")
    @app_commands.describe(emoji="Emoji du serveur")
    async def del_emoji(self, interaction: discord.Interaction, emoji: str):
        await interaction.response.defer()
        if not interaction.user.guild_permissions.manage_emojis and not interaction.user.id == owner_id:
            return await interaction.followup.send("Vous n'avais pas la permission ``manage_emojis``.", ephemeral=True) 
        elif not interaction.guild.get_member(self.bot.user.id).guild_permissions.manage_emojis:
            return await interaction.followup.send("Je n'ai pas la permission ``manage_emojis``.", ephemeral=True) 

        id_emoji = ''.join([n for n in emoji if n.isdigit()])

        try:
            emoji = await interaction.guild.fetch_emoji(id_emoji)
        except:
            return await interaction.followup.send("Cette emoji n'est pas présent sur le serveur.", ephemeral=True)

        await emoji.delete()
        await interaction.followup.send("L'emoji a été supprimer avec succès !", ephemeral=True)

async def setup(bot):
    await bot.add_cog(DELEMOJI(bot))