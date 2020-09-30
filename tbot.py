
# ====================================================================

# 입력받는 시간 5초 대기 - 확인
# [*]:조회, [!]:에러, [+]:db에 추가/수정,[-]: db에 삭제,[INFO]:로그에 추가 알림사항
# 언어는 영어로

# ====================================================================

import discord
import os
import asyncio
import itemlists

client = discord.Client()

@client.event
async def on_ready():
    #await client.change_presence(game=discord.Game(name="itemShop",type=1))
    print("Item shop")

@client.event
async def on_message(message):
    # 시험용 10점 넣기
    # db내 item 가져오기
    if message.content.startswith('!testupdate'):
        result=itemlists.testupdate(str(message.author))
        await message.channel.send(result)
        return 

    if message.content.startswith('!useitem'):
        result = itemlists.useitem(str(message.author))

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
                check_user = itemlists.checkMember(user_atk)
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
                result2 = itemlists.setStun(user_atk)
                 # stun 없애기
                itemlists.updateitem(str(message.author),"STUN;")
                await message.channel.send(result2)
                return

            elif user_res2 == 'REDEMPTION':
                # 문제 못풀었을 때 이동 가능
                result2 = itemlists.setRedemption(str(message.author))
                # redemption 없애기
                itemlists.updateitem(str(message.author),"REDEMPTION;")
                await message.channel.send(result2)
                return

            elif user_res2 == 'ASSASSIN':
                # 상대방 뒤로 옮기기
                result2 = itemlists.setAssassin(user_atk)
                # assassin 뒤로 옮기기
                itemlists.updateitem(str(message.author),"ASSASSIN;")
                await message.channel.send(result2)
                return

            elif user_res2 == "STEP": # STEP SKIP
                result2 = itemlists.updateitem(str(message.author),"STEP;")
                await message.channel.send(result2)
                return

            embed = discord.Embed(title="Check your answer",description=f"this is not right type '{user_res2}'")
            await message.channel.send(embed=embed)
            return

            '''
            elif user_res2 == "CAFFEINE": #보스레이드
                return
            elif user_res2 == "REDBULL": #보스레이드
                return
            elif user_res2 == "BOMB": #보스레이드
                return
            elif user_res2 == 'SNAKE': #snake의 기준은 뭐지 문서봐도 모르겠
                # 스네이크 없애기
                result2 = itemlists.updateitem(str(message.author),"SNAKE;")
                await message.channel.send("SNAKE")
                return
            '''
client.run(os.environ['token'])
