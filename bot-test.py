import discord
import os
import algoalgo_member

client = discord.Client()

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    # if this message is sent by bot itself, do nothing.
    if message.author == client.user:
        return
    
    # adduser function
    if message.content.startswith('!adduser'):
        result = algoalgo_member.adduser(str(message.author), message.content)
        await message.channel.send(result)
    
    # adduser function - admin
    if message.content.startswith('!admin_adduser'):
        result = algoalgo_member.adduser("admin", message.content)
        await message.channel.send(result)
    
    # have to add truncate table
    if message.content.startswith('!truncate'):
        result = algoalgo_member.truncate(message.content)
        await message.channel.send(result)
    
    if message.content.startswith('!showuserinfo'):
        result, userinfo = algoalgo_member.showuserinfo(message.author)
        embed = discord.Embed(title = f"USERINFO_{message.author}", description=userinfo, color = 0xffffff)
        await message.channel.send(result)
        await message.channel.send(embed=embed)

client.run("NzQ0MTE0NTUyMDczMDkzMTgy.Xzegrg.2bnBbWVMrIO48j2S8RMoT8KjTBo")
# client.run(os.environ['discord-token'])