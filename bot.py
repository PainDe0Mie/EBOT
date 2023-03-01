import discord, os, asyncio, random, time, requests
from commands.database.__init__ import db_connection, DATABASE_NAME, GET, SETUP, get, dbc_update
from colorama import Fore
from discord.ext import commands

# EBOT - {/} Slash Commands

# Bot make by PainDe0Mie#4811
# Email: painde0mie@gmail.com
# Github: https://github.com/PainDe0Mie/EBOT/

# "Questionnement" sur les 3 parametres ci-dessous.
EDIT_MODE = False

# Si le debug mode est désactiver, il ne réagira pas aux erreurs,
# or, si celui si est activer, il réagira normalement.
DEBUG_MODE = True
AUTO_RELOAD = True
AUTO_RELOAD_TIME = 600

# Si il a une erreur dans votre code, le message d'erreur sera envoyer dans un salon spécifique
# Mettre sur 0 si vous ne souhaitez pas envoyer d'erreur/de logs join.
ERROR_CHANNEL_ID = 0
JOIN_CHANNEL_ID = 0
YOUR_ID = 0

# Valeur à ne pas modifier !!
COMMANDS_LOAD = 0
MYSQL = False

# Connection à la base de donnée (MySql)

if db_connection.is_connected() == True:
    MYSQL = True

bot = commands.Bot(command_prefix = "e.", intents=discord.Intents().all())
bot.remove_command('help')

statuses = ["Slashs Commands", "ma bio !", "discord.gg/ebot", "axial-host.fr"]

if EDIT_MODE == True:
    dm = input('Démarer en debug mode ?\n> ')
    if dm == "True":
        DEBUG_MODE = True
    ar = input('Démarer avec l\'auto reload ?\n> ')
    if ar == "False":
        AUTO_RELOAD = False
    else:
        art = input('Temps avec de reload:\n> ')
        if art != "":
            AUTO_RELOAD_TIME = int(art)
            
@bot.event
async def on_ready():
    os.system('clear')
    print(f"Debug Mode: {DEBUG_MODE}\nAuto Reload: {AUTO_RELOAD}\nTemps: {AUTO_RELOAD_TIME}s\n\n")
    # Chargement des commandes (dans le dossier "./commands")
    global COMMANDS_LOAD
    ndc = len([name for name in os.listdir("commands") if os.path.isfile(os.path.join("commands", name))])
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name=f"Chargement..", type=3))
    print(Fore.YELLOW + f"Chargement de {ndc} commandes..")
    for name in os.listdir("commands"):
        if os.path.isfile(os.path.join("commands", name)):
            if DEBUG_MODE == False:
                try:
                    await bot.load_extension('commands.'+name[:-3])
                    print(Fore.GREEN + f'La commande "{name[:-3]}" a été chargée avec succès !')
                    COMMANDS_LOAD = COMMANDS_LOAD + 1
                except:
                    print(Fore.RED + f'La commande "{name[:-3]}" n\'a pas été chargée !')
            elif DEBUG_MODE == True:
                await bot.load_extension('commands.'+name[:-3])
                print(Fore.GREEN + f'La commande "{name[:-3]}" a été chargée avec succès !')
                COMMANDS_LOAD = COMMANDS_LOAD + 1
    print(Fore.RESET + str(COMMANDS_LOAD) + "/" + str(ndc) + " commandes chargées !")  
    await bot.tree.sync()
    bot.loop.create_task(statut_update())
    if MYSQL == True:
        print(Fore.GREEN + "\nConnecté à la base de donnée: " + Fore.RESET + f"\"{DATABASE_NAME}\"")
    else:
        print(Fore.RED + "\nConnecté à aucune base de donnée !")
    print(Fore.BLUE + f"Connecté en tant que {bot.user.name}#{bot.user.discriminator} !" + Fore.RESET)
    print("\nLogs:")
    bot.loop.create_task(dbc_update())
    
    # Mis à jours des commandes
    while AUTO_RELOAD:
        await asyncio.sleep(AUTO_RELOAD_TIME)
        for name in os.listdir("commands"):
            if os.path.isfile(os.path.join("commands", name)):
                if DEBUG_MODE == False:
                    try:
                        await bot.reload_extension('commands.'+name[:-3])
                    except:
                        pass
                else:
                    await bot.reload_extension('commands.'+name[:-3])
        await bot.tree.sync()

@bot.tree.command(description="Afficher la latence du bot.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Ping: {round(bot.latency*1000)}ms")
        
@bot.event
async def on_voice_state_update(member, before, after):
    try:
        if member == bot.user and member in after.channel.members:
            await member.guild.change_voice_state(channel=after.channel, self_deaf=True)
    except:
        pass
        
@bot.event
async def on_guild_join(guild):
    mc = 0
    for member in guild.members:
        if not member.bot:
            mc = mc + 1
                        
    if JOIN_CHANNEL_ID != 0:
        channel = bot.get_channel(JOIN_CHANNEL_ID)
        invitation = await random.choice(guild.text_channels).create_invite(reason="EBOT - Tanks to add me !", max_age=0, max_uses=0)
        embed = discord.Embed(description=f"**👑 Propriétaire:**\n {guild.owner.mention} - ({guild.owner.id})\n\n**Nombre de membres:**\n{mc}\n\n**🛬 Invitation :**\n[{invitation}]({invitation})")
        try:
            embed.set_author(name=f"J'ai rejoint {guild.name} ({guild.id})", icon_url=guild.icon.url)
        except:
            embed.set_author(name=f"J'ai rejoint {guild.name} ({guild.id})")
        await channel.send(embed=embed)
    
    try:
        SETUP(guild_id=guild.id)
    except:
        pass
    try:
        integrations = await guild.integrations()
    except:
        return

    if guild.owner_id == YOUR_ID:
        return
    
    for integration in integrations:
        if isinstance(integration, discord.BotIntegration):
            if integration.application.user.name == bot.user.name:
                if mc <= 20:
                    await integration.user.send("❌ Votre serveurs ne possèdent pas plus de 20 membres !")
                    await guild.leave()
                break
    
guild_update_counter = {}

@bot.event
async def on_guild_update(before, after):
    async for entry in after.audit_logs(limit=1, action=discord.AuditLogAction.guild_update):
        user = entry.user

    try:
        int(GET(after.id, "protect", "serveur")[0])
    except:
        return
    if user == bot.user or int(GET(after.id, "protect", "serveur")[0]) == 0 or str(user.id) in GET(after.id, "whitelist", "user_id") or after.owner == user:
        return
    else:
        guild_id = str(after.id)
        current_time = time.time()
        if guild_id in guild_update_counter:
            time_diff = current_time - guild_update_counter[guild_id]['time']
            if time_diff < 20:
                guild_update_counter[guild_id]['count'] += 1
            elif before.icon.url != after.icon.url and time_diff < 30:
                guild_update_counter[guild_id]['count'] += 1
            else:
                guild_update_counter[guild_id]['count'] = 0
        else:
            guild_update_counter[guild_id] = {'count': 0, 'time': current_time}

        if before.name != after.name:
            await after.edit(name=before.name)
            if guild_update_counter[guild_id]['count'] > 2:
                member = await after.fetch_member(user.id)
                del guild_update_counter[guild_id]
                for i in member.roles:
                    try:
                        await member.remove_roles(i)
                    except:
                        pass
                if GET(after.id, "protect", "logs")[0] != None:
                    LOGS = await bot.fetch_channel(int(GET(after.id, "protect", "logs")[0]))
                    embed = discord.Embed(description=f"<:attention:1071177877506236436> {user.mention} **a tenté à plusieurs reprises de modifier le nom du serveur !**", color=discord.Color.red())
                    embed.set_footer(text="Tout ces rôles ont été retirer. (Vous pouvez ajouter le membre dans la /whitelist)")
                    embed.set_author(name="Tentative de modification non autorisée", icon_url=bot.user.avatar.url)
                    await LOGS.send(embed=embed)
            elif GET(after.id, "protect", "logs") != None:
                LOGS = await bot.fetch_channel(int(GET(after.id, "protect", "logs")[0]))
                embed = discord.Embed(description=f"<:attention:1071177877506236436> {user.mention} **a tenté de modifier le nom du serveur !**", color=discord.Color.yellow())
                embed.set_footer(text="(Vous pouvez ajouter le membre dans la /whitelist)")
                embed.set_author(name="Tentative de modification non autorisée", icon_url=bot.user.avatar.url)
                await LOGS.send(embed=embed)
        elif before.icon.url != after.icon.url:
            response = requests.get(before.icon.url)
            icon = response.content
            await after.edit(icon=icon)
            if guild_update_counter[guild_id]['count'] > 2:
                member = await after.fetch_member(user.id)
                del guild_update_counter[guild_id]
                for i in member.roles:
                    try:
                        await member.remove_roles(i)
                    except:
                        pass
                if GET(after.id, "protect", "logs")[0] != None:
                    LOGS = await bot.fetch_channel(int(GET(after.id, "protect", "logs")[0]))
                    embed = discord.Embed(description=f"<:attention:1071177877506236436> {user.mention} **a tenté à plusieurs reprises de modifier l'icone du serveur !**", color=discord.Color.red())
                    embed.set_footer(text="Tout ces rôles ont été retirer. (Vous pouvez ajouter le membre dans la /whitelist)")
                    embed.set_author(name="Tentative de modification non autorisée", icon_url=bot.user.avatar.url)
                    await LOGS.send(embed=embed)
            elif GET(after.id, "protect", "logs") != None:
                LOGS = await bot.fetch_channel(int(GET(after.id, "protect", "logs")[0]))
                embed = discord.Embed(description=f"<:attention:1071177877506236436> {user.mention} **a tenté de modifier l'icone du serveur !**", color=discord.Color.yellow())
                embed.set_footer(text="(Vous pouvez ajouter le membre dans la /whitelist)")
                embed.set_author(name="Tentative de modification non autorisée", icon_url=bot.user.avatar.url)
                await LOGS.send(embed=embed)
        elif after.premium_tier >= 2 and before.banner.url != after.banner.url:
            response = requests.get(before.banner.url)
            banner = response.content
            await after.edit(banner=banner)
            if guild_update_counter[guild_id]['count'] > 2:
                member = await after.fetch_member(user.id)
                del guild_update_counter[guild_id]
                for i in member.roles:
                    try:
                        await member.remove_roles(i)
                    except:
                        pass
                if GET(after.id, "protect", "logs")[0] != None:
                    LOGS = await bot.fetch_channel(int(GET(after.id, "protect", "logs")[0]))
                    embed = discord.Embed(description=f"<:attention:1071177877506236436> {user.mention} **a tenté à plusieurs reprises de modifier l'arrière plan du serveur !**", color=discord.Color.red())
                    embed.set_footer(text="Tout ces rôles ont été retirer. (Vous pouvez ajouter le membre dans la /whitelist)")
                    embed.set_author(name="Tentative de modification non autorisée", icon_url=bot.user.avatar.url)
                    await LOGS.send(embed=embed)
            elif GET(after.id, "protect", "logs") != None:
                LOGS = await bot.fetch_channel(int(GET(after.id, "logs")[0]))
                embed = discord.Embed(description=f"<:attention:1071177877506236436> {user.mention} **a tenté de modifier l'arrière plan du serveur !**", color=discord.Color.yellow())
                embed.set_footer(text="(Vous pouvez ajouter le membre dans la /whitelist)")
                embed.set_author(name="Tentative de modification non autorisée", icon_url=bot.user.avatar.url)
                await LOGS.send(embed=embed)
        elif after.premium_tier >= 1 and before.splash.url != after.splash.url:
            response = requests.get(before.splash.url)
            splash = response.content
            await after.edit(splash=splash)
            if guild_update_counter[guild_id]['count'] > 2:
                member = await after.fetch_member(user.id)
                del guild_update_counter[guild_id]
                for i in member.roles:
                    try:
                        await member.remove_roles(i)
                    except:
                        pass
                if GET(after.id, "protect", "logs")[0] != None:
                    LOGS = await bot.fetch_channel(int(GET(after.id, "protect", "logs")[0]))
                    embed = discord.Embed(description=f"<:attention:1071177877506236436> {user.mention} **a tenté à plusieurs reprises de modifier l'arrière plan d'invitation du serveur !**", color=discord.Color.red())
                    embed.set_footer(text="Tout ces rôles ont été retirer. (Vous pouvez ajouter le membre dans la /whitelist)")
                    embed.set_author(name="Tentative de modification non autorisée", icon_url=bot.user.avatar.url)
                    await LOGS.send(embed=embed)
            elif GET(after.id, "protect", "logs") != None:
                LOGS = await bot.fetch_channel(int(GET(after.id, "logs")[0]))
                embed = discord.Embed(description=f"<:attention:1071177877506236436> {user.mention} **a tenté de modifier l'arrière plan d'invitation du serveur !**", color=discord.Color.yellow())
                embed.set_footer(text="(Vous pouvez ajouter le membre dans la /whitelist)")
                embed.set_author(name="Tentative de modification non autorisée", icon_url=bot.user.avatar.url)
                await LOGS.send(embed=embed)

async def statut_update():
    statuses.append(f"{len(bot.guilds)} serveurs 🎈")
    while True:
        await bot.wait_until_ready()
        while not bot.is_closed():
            status = random.choice(statuses)
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))
            await asyncio.sleep(10)

bot.run(get("ebot"))