import discord, asyncio
from discord import app_commands
from discord.ext import commands

class NUKE(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Recréer le salon en supprimant l'ancien.")
    @commands.has_permissions(manage_channels=True)
    async def nuke(self, interaction: discord.Interaction, channel: discord.TextChannel=None):
        await interaction.response.defer()
        nuke = discord.Embed(title="🧨 Salon nuke !")

        if interaction.user.guild_permissions.manage_channels:
            if channel == None:

                nuke_channel = discord.utils.get(interaction.guild.channels, name=interaction.channel.name)
                position = nuke_channel.position

                new_channel = await nuke_channel.clone(reason=f"/nuke {nuke_channel.name} | Effectuer par {interaction.user.name}#{interaction.user.discriminator}")

                await nuke_channel.delete()
                await new_channel.edit(position=position)

                try:
                    await interaction.followup.send(f"Le salon {new_channel.mention} a été nuke avec succès !")
                except:
                    pass

            else:
                nuke_channel = discord.utils.get(interaction.guild.channels, name=channel.name)
                position = nuke_channel.position

                if nuke_channel is not None:
                
                    new_channel = await nuke_channel.clone(reason=f"/nuke {nuke_channel.name} | Effectuer par {interaction.user.name}#{interaction.user.discriminator}")

                    await nuke_channel.delete()
                    await new_channel.edit(position=position)

                    msg = await new_channel.send(embed=nuke)
                    await asyncio.sleep(2)
                    await msg.delete()

                    try:
                        await interaction.followup.send(f"Le salon {new_channel.mention} a été nuke avec succès !")
                    except:
                        pass

                else:
                    await interaction.followup.send(f"❌ Le salon {channel.name} n'a pas été trouvé !")
        else:
            await interaction.followup.send("❌ Vous n'avez pas la permission de gérer les salons !")

async def setup(bot):
    await bot.add_cog(NUKE(bot))