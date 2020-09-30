import discord
from discord.ext import commands
import algoalgo_map
import os

client = commands.Bot(command_prefix = '-')
admin = 742625793276116992

@client.event 
async def on_ready():
    await client.change_presence(status=discord.Status.online)
    await client.change_presence(activity=discord.Game(name="당신의 위치를 파악"))
    print("봇 이름:",client.user.name,"봇 아이디:",client.user.id,"봇 버전:",discord.__version__)

@client.event
async def on_message(message):
    # if this message is sent by bot itself, do nothing.
    if message.author == client.user:
        return
    
    #player's location
    if message.content.startswith('!show_map'):
        await message.channel.send('Loading...Map..')
        result, Locinfo = algoalgo_map.showmap(message.author)
        embed = discord.Embed(title = f"""== **{message.author}** 's location ==""", description=Locinfo, color = 0x6b9560)
        await message.channel.send(result)
        await message.channel.send(embed=embed)
    
    #admin :: set map feature
    if message.content.startswith('!set_map'):
        result = f"[*] the admin permission required."
        if message.author.top_role.id == admin:
            result = algoalgo_map.setmap(message.content)
        await message.channel.send(result)

    #admin :: getLocType
    if message.content.startswith('!getLocType'):
        result = f"""[*] the admin permission required."""
        embed = discord.Embed(title = f"""[*] the admin permission required.""", description=f"""your role :: {message.author.top_role.name}""", color = 0x00aaaa)
        if message.author.top_role.id == admin:
            result, LocFeatureInfo, nowLoc = algoalgo_map.getLocType(message.content)
            embed = discord.Embed(title = f"""== the feature of the **{nowLoc}** location ==""", description=LocFeatureInfo, color = 0x6b9560)
        await message.channel.send(result)
        await message.channel.send(embed=embed)

    #admin :: getPlayers
    if message.content.startswith('!getPlayers'):
        result = f"""[*] the admin permission required."""
        embed = discord.Embed(title = f"""[*] the admin permission required.""", description=f"""your role :: {message.author.top_role.name}""", color = 0x00aaaa)
        if message.author.top_role.id == admin:
            result , Locinfo, nowLoc = algoalgo_map.getPlayers(message.content)
            embed = discord.Embed(title = f"""== the player list in the **{nowLoc}** location ==""", description=Locinfo, color = 0x6b9560)
        await message.channel.send(result)
        await message.channel.send(embed=embed)
        
    #admin ::  printing the highest role 
    if message.content.startswith('!role_id'):
        await message.channel.send(embed=discord.Embed(title=f"""== {message.author}'s the highest role INFO ==""", description = f""" the highest role :: {message.author.top_role.name}\n the highest role id :: {message.author.top_role.id} """, color = 0x6b9560))


    #admin ::  printing all_role id 
    if message.content.startswith('!all_roles_id'):
        for i in range(len(message.author.roles)):
            await message.channel.send(embed=discord.Embed(title=f"""== {message.author}'s the roles INFO ==""", description = f""" the role #{i} :: {message.author.roles[i].name}\n the role #{i}'s' id :: {message.author.roles[i].id} """, color = 0x6b9560))
         
client.run(os.environ['token_map'])