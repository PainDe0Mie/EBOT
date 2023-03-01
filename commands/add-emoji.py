import discord, os
from discord import app_commands
from discord.ext import commands

owner_id = 956183732841250946

class ADDEMOJI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Ajouter un emoji sur votre serveur.")
    @app_commands.describe(data="Emoji ou image (url)")
    async def add_emoji(self, interaction: discord.Interaction, nom: str, data: str):
        await interaction.response.defer()
        if not interaction.user.guild_permissions.manage_emojis and not interaction.user.id == owner_id:
            return await interaction.followup.send("Vous n'avais pas la permission ``manage_emojis``.", ephemeral=True) 
        elif not interaction.guild.get_member(self.bot.user.id).guild_permissions.manage_emojis:
            return await interaction.followup.send("Je n'ai pas la permission ``manage_emojis``.", ephemeral=True) 


        gif_url = ""

        if "https://" in data:
            image_url = data
        else:
            id_emoji_o = ''.join([n for n in data if n.isdigit()])
            if ":" in data[-20]:
                id_emoji = id_emoji_o[-18:]
            elif ":" in data[-21]:
                id_emoji = id_emoji_o[-19:]

            if "a" in data[1]: 
                gif_url = "https://cdn.discordapp.com/emojis/" + id_emoji + ".gif?size=44&quality=lossless"
            else:
                image_url = "https://cdn.discordapp.com/emojis/" + id_emoji + ".png?size=44&quality=lossless"
                    
                    
        import requests

        if gif_url != "":
            img_data = requests.get(gif_url).content
            with open(f'{interaction.guild.id}_emoji.gif', 'wb') as handler:
                handler.write(img_data)

            with open(f'{interaction.guild.id}_emoji.gif', 'rb') as f:
                gif = f.read()
        else:
            img_data = requests.get(image_url).content
            with open(f'{interaction.guild.id}_emoji.png', 'wb') as handler:
                handler.write(img_data)

            with open(f'{interaction.guild.id}_emoji.png', 'rb') as f:
                image = f.read()

        if gif_url != "":
            emoji = await interaction.guild.create_custom_emoji(name=nom, image=gif)
            os.remove(f'{interaction.guild.id}_emoji.gif')
        else:
            emoji = await interaction.guild.create_custom_emoji(name=nom, image=image)
            os.remove(f'{interaction.guild.id}_emoji.png')

        await interaction.followup.send(f"L'emoji {emoji} a été créer avec succes !", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ADDEMOJI(bot))