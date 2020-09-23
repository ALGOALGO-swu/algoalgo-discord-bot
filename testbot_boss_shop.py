import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot
import algoalgo_shop

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    print("디스코드 봇 로그인이 완료되었습니다.")
    print("디스코드봇 이름:" + client.user.name)
    print("디스코드봇 ID:" + str(client.user.id))
    print("디스코드봇 버전:" + str(discord.__version__))
    print('------')
    await client.change_presence(status=discord.Status.online, activity=discord.Game("보스샵 쇼핑"))

@client.event
async def on_message(message):
    # show boss shop items detail info
    if message.content.startswith('!boss_shop'):
        embed = discord.Embed(title="ALGOALGO BOSS SHOP BOT",description="BOSS SHOP 아이템 목록", color=0x00aaaa, inline=True)
        embed.add_field(name="CAFFEINE🍺", value="3포인트. 본인의 다음 공격 데미지가 2배가 됩니다", inline=False)
        embed.add_field(name="REDBULL💊", value="5포인트. 본인의 다음 공격 데미지가 3배가 됩니다", inline=False)
        embed.add_field(name="BOMB💣", value="6포인트. 구매 즉시 자동 사용으로, 보스에게 100 데미지 공격을 합니다", inline=False)
        await message.channel.send(embed=embed)
        #await message.channel.send("Please enter the item you want\CAFFEINE🍺, REDBULL💊, BOMB💣\nUsage: !buybossitem <item name> <number>")
        msg = await message.channel.send("원하는 아이템 이모지를 클릭하세요")
        await msg.add_reaction("🍺") #caffeine
        await msg.add_reaction("💊") #red bull
        await msg.add_reaction("💣") #bomb
        
        def check(reaction, user):
            return user == message.author and (str(reaction.emoji) == '🍺' or str(reaction.emoji) == '💊' or str(reaction.emoji) == '💣')
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await message.channel.send('👎')
        else:
            #await message.channel.send('👍')
            whatemoji=""
            if str(reaction.emoji) == '🍺':
                whatemoji="CAFFEINE"
            elif str(reaction.emoji) == '💊':
                whatemoji="REDBULL"
            elif str(reaction.emoji) == '💣':
                whatemoji="BOMB"
            
            result, pointinfo = algoalgo_shop.point_check(message.author)
            await message.channel.send("현재 보유 포인트: "+pointinfo)
            if int(pointinfo)>0:
                gogo = "!buyitem "+whatemoji+" 1"
                result = algoalgo_shop.buy_item(str(message.author), gogo)
                await message.channel.send(result)
            else:
                await message.channel.send("포인트가 부족합니다. 구매를 종료합니다")

client.run('-')
