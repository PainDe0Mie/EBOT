import discord
from discord import app_commands
from discord.ext import commands

owner_id = 956183732841250946

class DELSTICKER(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Supprimer un autocollant sur votre serveur.")
    @app_commands.describe(id="Autocollant du serveur")
    async def del_sticker(self, interaction: discord.Interaction, id: str):
        await interaction.response.defer()
        if not interaction.user.guild_permissions.manage_emojis_and_stickers and not interaction.user.id == owner_id:
            return await interaction.followup.send("Vous n'avais pas la permission ``manage_emojis_and_stickers``.", ephemeral=True) 
        elif not interaction.guild.get_member(self.bot.user.id).guild_permissions.manage_emojis:
            return await interaction.followup.send("Je n'ai pas la permission ``manage_emojis_and_stickers``.", ephemeral=True) 

        try:
            autocollant = await interaction.guild.fetch_sticker(int(id))
        except:
            return await interaction.followup.send("Cette autocollant n'est pas présent sur le serveur.", ephemeral=True)

        await interaction.guild.delete_sticker(autocollant)
        await interaction.followup.send("L'autocollant a été supprimer avec succès !", ephemeral=True)

async def setup(bot):
    await bot.add_cog(DELSTICKER(bot))