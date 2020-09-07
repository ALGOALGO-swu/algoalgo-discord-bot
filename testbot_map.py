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
    
    #show map feature
    if message.content.startswith('!show_map'):
        await message.channel.send('Loading...Map..')
    
    #set map feature
    if message.content.startswith('!set_map'):
        result = algoalgo_map.setmap(message.content)
        await message.channel.send(result)
    

client.run(os.environ['token_map'])
