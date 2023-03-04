import discord, requests, os
import emoji as emote
from discord import app_commands
from discord.ext import commands

owner_id = 956183732841250946

class ADDSTICKER(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Ajouter un emoji sur votre serveur.")
    @app_commands.describe(data="(url) Image au format: PNG, APNG")
    @app_commands.describe(emoji="Emoji par default")
    async def add_sticker(self, interaction: discord.Interaction, nom: str, emoji: str, data: str):
        await interaction.response.defer()
        if not interaction.user.guild_permissions.manage_emojis_and_stickers and not interaction.user.id == owner_id:
            return await interaction.followup.send("Vous n'avais pas la permission ``manage_emojis_and_stickers``.", ephemeral=True) 
        elif not interaction.guild.get_member(self.bot.user.id).guild_permissions.manage_emojis:
            return await interaction.followup.send("Je n'ai pas la permission ``manage_emojis_and_stickers``.", ephemeral=True) 

        if not emote.emoji_count(emoji) > 0:
            return await interaction.followup.send("Vous devez entrer un emoji par default !", ephemeral=True) 

        if not ".png" in data or not ".apng" in data:
            return await interaction.followup.send("Le format de votre image est incompatible ! (png ou apng)", ephemeral=True) 

        try:
            img_data = requests.get(data)
            with open(f'{interaction.guild.id}_autocollant.png', 'wb') as handler:
                handler.write(img_data)
        except:
            return await interaction.followup.send("Votre url est invalide !", ephemeral=True) 

        await interaction.guild.create_sticker(name=nom, description=nom + f" made by {interaction.user.name}#{interaction.user.discriminator}", emoji=emoji, file=discord.File(f'{interaction.guild.id}_autocollant.png'))
        os.remove(f'{interaction.guild.id}_autocollant.png')

        await interaction.followup.send(f"L'autocollant a été créer avec succes !", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ADDSTICKER(bot))
