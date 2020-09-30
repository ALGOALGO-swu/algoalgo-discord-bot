import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import algoalgo_member
import algoalgo_shop
import algoalgo_item
import algoalgo_map

client = discord.Client()
admin = 742625793276116992


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    print("디스코드 봇 로그인이 완료되었습니다.")
    print("디스코드봇 이름:" + client.user.name)
    print("디스코드봇 ID:" + str(client.user.id))
    print("디스코드봇 버전:" + str(discord.__version__))
    print('------')
    await client.change_presence(status=discord.Status.online, activity=discord.Game("GM on Board (feat. algorithm)"))

@client.event
async def db_refresh():
    print(datetime.now())
    algoalgo_member.refresh()

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
    
    # show user info
    if message.content.startswith('!showuserinfo'):
        result, userinfo = algoalgo_member.showuserinfo(message.author)
        embed = discord.Embed(title = f"USERINFO_{message.author}", description=userinfo, color = 0xffffff)
        await message.channel.send(result)
        await message.channel.send(embed=embed)

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


    # show items detail info
    if message.content.startswith('!showshopinfo'):
        embed = discord.Embed(title="ALGOALGO SHOP BOT",description="SHOP 아이템 목록", color=0x00aaaa, inline=True)
        embed.add_field(name="STEP🦶", value="저희 게임 일반 모드에서의 전진 아이템입니다. 보드 판 위의 문제(백준 알고리즘 문제)를 해결 했을 때, 앞으로 1칸 전진할 수 있는 기회를 제공해주는 아이템입니다. 하루 최대 2개 까지 구매가능 합니다. 다만, 두 번째 구매시엔 가격이 두 배로(10pt로) 상승합니다. 즉, 하루에 STEP을 사용하여 2칸까지 전진할 수 있습니다.", inline=False)
        embed.add_field(name="THE ALGOALGO REDEMPTION🛡", value="저희 게임 일반 모드에서의 방어 아이템입니다. 보드 판 위의 문제(백준 알고리즘 문제)를 해결하지 못했을 때의 상황을 모면하는 아이템 입니다. REDEMPTION을 사용하면, 문제를 해결하지 못해도 STEP을 사용하여 전진할 수 있게 됩니다. 하루 최대 1개 까지 구매가능 합니다.", inline=False)
        embed.add_field(name="SNAKE HUNTER🐍", value="저희 게임 일반 모드에서의 방어 아이템입니다. 저희 게임 맵은 뱀사다리 게임의 보드판을 표방합니다. 게임 진행 시 뱀으로 인한 후퇴 상황을 막아줍니다. 게임이 진행될 수록, 가격이 하락합니다.", inline=False)
        embed.add_field(name="ASSASSIN ALGOALGO🗡", value="저희 게임 일반 모드에서의 타 플레이어 방해 아이템입니다. N개의 아이템 사용으로, 유저 한 명을 N칸 후퇴시킬 수 있습니다.", inline=False)
        embed.add_field(name="STUN⚔️", value="저희 게임 일반 모드에서의 타 플레이어 방해 아이템입니다. 유저 한명의 아이템 STEP 사용을 막아 전진을 못하게 합니다.", inline=False)
        embed.add_field(name="CAFFEINE🍺", value="저희 게임 보스레이드 모드에서의 버프 아이템입니다. 본인의 공격을 2배로 늘릴 수 있습니다.", inline=False)
        embed.add_field(name="REDBULL💊", value="저희 게임 보스레이드 모드에서의 버프 아이템입니다. 본인의 공격을 3배로 늘릴 수 있습니다.", inline=False)
        embed.add_field(name="BOMB💣", value="저희 게임 보스레이드 모드에서의 보스 공격 아이템입니다. 구매 즉시 보스에게 100 데미지를 주게됩니다. 다만 각 개인들은 해당 아이템을 5개 까지만 구매 가능합니다.", inline=False)
        await message.channel.send(embed=embed)
        await message.channel.send("Please enter the item you want\nSTEP🦶, REDEMPTION🛡, SNAKE🐍, ASSASSIN🗡, STUN⚔️\nUsage: Usage: !buyitem <item name> <number>")

    # show shop items info
    if message.content.startswith('!shop'):
        embed = discord.Embed(title="유후! 여름 빅 세일입니다\nSTEP과 STUN, 제가 직접 만든 SNAKE도 반값 할인 중입니다")
        embed.set_image(url="https://blog.kakaocdn.net/dn/b4numP/btqIrvqfcvg/Hm88ead0XHCjQnyKjoSO91/img.png")
        embed.add_field(name="STEP🦶", value="3pt", inline=True)
        embed.add_field(name="REDEMPTION🛡", value="5pt", inline=True)
        embed.add_field(name="SNAKE🐍", value="10pt", inline=True)
        embed.add_field(name="ASSASSIN🗡", value="6pt", inline=True)
        embed.add_field(name="STUN⚔️", value="6pt", inline=True)
        await message.channel.send(embed=embed)
        await message.channel.send("**지금 당장 구매하세요!** -->> !buyitem <item name> <number>")

    # buy items 
    if message.content.startswith('!buyitem'):
        result, pointinfo = algoalgo_shop.point_check(message.author)
        await message.channel.send("현재 보유 포인트: "+pointinfo)
        if int(pointinfo)>0:
            result = algoalgo_shop.buy_item(str(message.author), message.content)
            await message.channel.send(result)
        else:
            await message.channel.send("포인트가 부족합니다. 구매를 종료합니다")

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
    

    #admin ::  printing all_role id 
    if message.content.startswith('!step'):
        result, feature, daily = algoalgo_map.step(message.author)
        # embed = discord.Embed(title = f"""== **{message.author}** 's location ==""", description=Locinfo, color = 0x6b9560)
        await message.channel.send(result)
        await message.channel.send(embed=embed)

    if message.content.startswith('!useitem'):
        result = algoalgo_item.useitem(str(message.author))

        #아이템 목록 출력하는 칸임
        if result == 0:
            embed = discord.Embed(title="NO Item",description="please buy item first")
            await message.channel.send(embed=embed)
            return
        else:
            await message.channel.send("item 목록")
            await message.channel.send(result)
            

        embed = discord.Embed(title="Ha ha, What do you want?", description="5초 안에 아이템 번호를 입력해주세요")
        embed.add_field(name='**사용법**',value='**사용하고자 할 아이템 번호를 입력해주세요. 단, assassin, stun, bomb는 번호와 유저이름을 입력**',inline=False)
        embed.add_field(name='**예시**',value='**`1`, `2`,`3`,`1 kim`,`3 park`**',inline=False)
        channel = message.channel
        await message.channel.send(embed=embed)
        
        def buy(mes):
            return mes.author == message.author and mes.channel and channel
        try:
            msg = await client.wait_for('message',timeout=10.0, check=buy) 
        except asyncio.TimeoutError:
            embed = discord.Embed(title="TIME OUT",description="oh you don't need it? oKay... BYE!")
            await message.channel.send(embed=embed)
            return
        else:
            # 사용자 입력값 검사
            if len(msg.content) < 2: # 입력값 검사
                 user_res = int(msg.content) 
                 #await message.channel.send("input")

            else:
                # await message.channel.send("input check")
                tmp = msg.content.split() #입력값 공백 기준으로 나누기
                user_res = int(tmp[0]) # user_res = 아이템 인덱스
                user_atk = tmp[1] # user_atk = 공격받는 유저
                
                # 받은 값 중 올바른 사용자를 입력받았는지 검사해야함
                check_user = algoalgo_item.checkMember(user_atk)
                #print(check_user)
                if not check_user:
                    embed = discord.Embed(title="Check userID",description=f"there isn't name '{user_atk}'")
                    await message.channel.send(embed=embed)
                    return
            

            await message.channel.send(user_res)
            user_res2 = result[user_res][0] # user_res2 = 아이템 명
            #print(user_res2)
            if user_res2 == 'STUN':
                # 상대방 status = -1 로 업데이트
                result2 = algoalgo_item.setStun(user_atk)
                 # stun 없애기
                algoalgo_item.updateitem(str(message.author),"STUN;")
                await message.channel.send(result2)
                return

            elif user_res2 == 'REDEMPTION':
                # 문제 못풀었을 때 이동 가능
                result2 = algoalgo_item.setRedemption(str(message.author))
                # redemption 없애기
                algoalgo_item.updateitem(str(message.author),"REDEMPTION;")
                await message.channel.send(result2)
                return

            elif user_res2 == 'ASSASSIN':
                # 상대방 뒤로 옮기기
                result2 = algoalgo_item.setAssassin(user_atk)
                # assassin 뒤로 옮기기
                algoalgo_item.updateitem(str(message.author),"ASSASSIN;")
                await message.channel.send(result2)
                return

            elif user_res2 == "STEP": # STEP SKIP
                #성공
                result, feature, daily = algoalgo_map.step(message.author)

                if feature == 2 : # 뱀
                    embed = discord.Embed(title="Snake!",description="do you want to run? YES or NO")
                    embed.add_field(name='**SNAKE**',value='snake가 있을 시 YES 없는 경우 NO',inline=False)
                    await message.channel.send(embed=embed)

                    def use(mes):
                        return mes.author == message.author and mes.channel and channel
                    try:
                        msg = await client.wait_for('message',timeout=10.0, check=use) 
                    except asyncio.TimeoutError:
                        embed = discord.Embed(title="TIME OUT",description="oh you don't want it? oKay... BYE!")
                        await message.channel.send(embed=embed)
                        return
                    else:
                        # 사용자 입력값 검사
                        if msg.content == "NO": 
                            result2 = algoalgo_map.snake(message.author)
                            await message.channel.send(result)
                        else:
                            embed = discord.Embed(title="당신은 무사!",description="뱀을 피하고 잘 도착!")
                            await message.channel.send(embed=embed)
                            return

                elif feature == 1: # 1이 사다리
                    embed = discord.Embed(title="일반 칸",description="잘 도착했네요")
                    await message.channel.send(embed=embed)
                    return
                    

                elif feature == 0: # 0이 일반
                    embed = discord.Embed(title="사다리 칸",description="축하해요 사다리 칸에 도착했네요")
                    await message.channel.send(embed=embed)
                    return


                result2 = algoalgo_item.updateitem(str(message.author),"STEP;")
                await message.channel.send(result2)
                return

            embed = discord.Embed(title="Check your answer",description=f"this is not right type '{user_res2}'")
            await message.channel.send(embed=embed)
            return

            


sched = AsyncIOScheduler()
sched.add_job(db_refresh, 'cron', hour=0)
sched.start()

client.run(os.environ['discord-token'])

