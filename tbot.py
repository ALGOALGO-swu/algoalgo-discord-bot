import discord
import os
import asyncio
import itemlists

client = discord.Client()

@client.event
async def on_ready():
    #await client.change_presence(game=discord.Game(name="itemShop",type=1))
    print("this is item shop. welcome!")

@client.event
async def on_message(message):
    if message.content.startswith('!useitem'):
        result = itemlists.useitem(str(message.author))
        await message.channel.send('Ha ha, What do you want?')
        await message.channel.send(result)
        
client.run(os.environ['token'])
