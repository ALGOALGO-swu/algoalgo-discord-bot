import discord
import os
import algoalgo_member
import member
from apscheduler.schedulers.background import BackgroundScheduler

REFRESH_TIME = '5'

client = discord.Client()

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    # if this message is sent by bot itself, do nothing.
    if message.author == client.user:
        return
    
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('!refresh'):
        result = member.refresh()
        await message.channel.send(result)

    if message.content.startswith('!addpoint'):
        result = member.addpoint(message.content)
        await message.channel.send(result)

    if message.content.startswith('!list_achievement'):
        result = member.list_achievement()
        embed = discord.Embed(title="Achievement List", description=result, color=0xffffff)
        await message.channel.send(embed=embed)

    # adduser function
    if message.content.startswith('!adduser'):
        result = algoalgo_member.adduser(str(message.author), message.content)
        await message.channel.send(result)

    # have to add truncate table
    if message.content.startswith('!truncate'):
        result = algoalgo_member.truncate(message.content)
        await message.channel.send(result)

    if message.content.startswith('!showuserinfo'):
        result, userinfo = algoalgo_member.showuserinfo(message.author)
        embed = discord.Embed(title=f"USERINFO_{message.author}", description=userinfo, color=0xffffff)
        await message.channel.send(result)
        await message.channel.send(embed=embed)


client.run(os.environ['discord-token'])