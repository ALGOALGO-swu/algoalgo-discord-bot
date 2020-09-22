import discord
from discord.ext import commands
import algoalgo_map
import os

client = commands.Bot(command_prefix = '-')

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
    
    #set map feature
    if message.content.startswith('!set_map'):
        result = algoalgo_map.setmap(message.content)
        await message.channel.send(result)
    
    # 역할 id 반환
    if message.content.startswith('!role_id'):
        for i in range(len(message.guild.roles)):
            Ridlist = ""
            Ridlist += message.guild.roles[i].id
            await message.channel.send(Ridlist)


    # if message.content.startswith('!set_map'):
    #     # admin = message.author.roles.find
    #     # admin = discord.utils.get(ctx.guild.roles, name = "db_admin")
        
    #     result = f"[*] the permission required."
    #     # if message.author.roles.has('db_admin')
    #     # if message.guild.get in get(ctx.guild.roles, name = "db_admin").members:
    #     # if get(ctx.guild.roles, name = "db_admin") in discord.member.roles:
            
    #     if (message.author.guild_permissions.administrator):
    #         try:
    #             result = algoalgo_map.setmap(message.content)
    #         except Exception as e:
    #             await message.channel.send(embed=discord.Embed(title="에러 발생", description = str(e), color = 0xff0000))
    #     else:
    #         await message.channel.send(embed=discord.Embed(title="권한 부족", description = message.author.mention + "님은 채널을 관리 할 수 있는 권한이 없습니다.", color = 0xff0000))
    #     await message.channel.send(result)


    #test :: getLocType
    if message.content.startswith('!getLocType'):
        result, LocFeatureInfo, nowLoc = algoalgo_map.getLocType(message.content)
        embed = discord.Embed(title = f"""== the feature of the **{nowLoc}** location ==""", description=LocFeatureInfo, color = 0x6b9560)
        await message.channel.send(result)
        await message.channel.send(embed=embed)

    #test :: getPlayers
    if message.content.startswith('!getPlayers'):
        result , Locinfo, nowLoc = algoalgo_map.getPlayers(message.content)
        embed = discord.Embed(title = f"""== the player list in the **{nowLoc}** location ==""", description=Locinfo, color = 0x6b9560)
        await message.channel.send(result)
        await message.channel.send(embed=embed)
    

client.run(os.environ['token_map'])