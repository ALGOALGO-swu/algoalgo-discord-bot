import discord
import os
import algoalgo_member
from apscheduler.schedulers.background import BackgroundScheduler

REFRESH_TIME = '5'

client = discord.Client()
admin = 742625793276116992

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
        result = f"[!] Admin Permission Required."
        if message.author.top_role.id == admin:
            result = algoalgo_member.refresh()
        await message.channel.send(result)

    if message.content.startswith('!addpoint'):
        result = f"[!] Admin Permission Required."
        if message.author.top_role.id == admin:
            result = algoalgo_member.addpoint(message.content)
        await message.channel.send(result)

    if message.content.startswith('!list_achievement'):
        result = algoalgo_member.list_achievement()
        if result.split()[0] != '[!]':
            embed = discord.Embed(title="Achievement List", description=result, color=0xffffff)
            await message.channel.send(f"[*] Successfully Inquired Achievement List")
            await message.channel.send(embed=embed)
        else:
            await message.channel.send(result)

    if message.content.startswith('!random_bj'):
        result = algoalgo_member.random_bj(str(message.author), message.content)
        if result.split()[0] != '[!]':
            embed = discord.Embed(title="Try This!", description=result, color=0xffffff)
            await message.channel.send(f"[*] Successfully Found A Random Baekjoon Problem")
            await message.channel.send(embed=embed)
        else:
            await message.channel.send(result)

    if message.content.startswith('!daily_baekjoon'):
        result = algoalgo_member.daily_baekjoon(str(message.author), message.content)
        await message.channel.send(result)

    if message.content.startswith('!unlock'):
        result = algoalgo_member.unlock(str(message.author))
        await message.channel.send(result)
"""
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
"""

# client.run(os.environ['discord-token'])
client.run()