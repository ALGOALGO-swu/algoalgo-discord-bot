
# ====================================================================
# 해야할 것 (데이터베이스 구현 참고)
# 인덱스 번호로 입력받아 아이템 사용하게 하기 - 확인
# 아이템의 유무 확인 검사 - 확인
# 걱정되는 것: 이미 함수 실행 중인데 다시 input값을 받아 사용할 수 있는가?  - 확인
# https://blog.yonghyeon.com/9 해당 블로그 참고: 사용자에게 다시 입력받기 활용 예제 - 가위바위보
# 입력받는 시간 5초 대기 - 확인
# [*]:조회, [!]:에러, [+]:db에 추가/수정,[-]: db에 삭제,[INFO]:로그에 추가 알림사항
# 언어는 영어로

# 추가사항
# 사용자의 입력값 검사하기: DB에 이사람 공격할건데 있으신분인지 물어보기
# 공통함수 작성하기: 아이템 사용 후 db update구문으로 삭제 반영
# 아이템 사용: 상대방 및 자기 dB에 변경사항 업데이트
# snake 친구
# snake 가 어떤식으로 이뤄지는지..?
# 문제풀고->스텝 사용-> 도착-> 스네이크다! -> 이동-> 스네이크 변수를(따로 생성해야함) 검사하여 이동된거면 item사용하여 이전 기록으로 되돌림?-> 근데 이전 기록은 어떻게 저장되서 로드되는지? 

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
    if message.content.startswith('!useitem'):
        result = itemlists.useitem(str(message.author))
        if result == 0:
            message.channel.send("empty.......")
            return
        embed = discord.Embed(title="Ha ha, What do you want?", description="choose your item 'number' in 5sec")
        embed.add_field(name='**사용법**',value='**사용하고자 할 아이템 번호를 입력해주세요. 단, assassin, stun, bomb는 번호와 유저이름을 입력**',inline=False)
        embed.add_field(name='**예시**',value='**`1`, `2`,`3`,`1 kim`,`3 park`**',inline=False)
        channel = message.channel
        await message.channel.send(embed=embed)
        def buy(mes):
            return mes.author == message.author and mes.channel and channel
        try:
            msg = await client.wait_for('message',timeout=5.0, check=buy) 
        except asyncio.TimeoutError:
            embed = discord.Embed(title="TIME OUT",description="oh you don't need it? oKay... BYE!")
            await message.channel.send(embed=embed)
            return
        else:
            # 사용자 입력값 검사
            if len(msg.content) < 2: # 입력값 검사
                 user_res = int(msg.content) 

            elif len(msg.content) == 2: 
                tmp = msg.content.split() #입력값 공백 기준으로 나누기
                user_res = int(tmp[0]) # user_res = 아이템 인덱스
                user_atk = tmp[1] # user_atk = 공격받는 유저
                
                # 받은 값 중 올바른 사용자를 입력받았는지 검사해야함
                check_user = itemlists.checkMember(user_atk)
                if check_user == False:
                    embed = discord.Embed(title="Check userID",description="there isn't name '{user_atk}'")
                    await message.channel.send(embed=embed)
                    return
            else:
                embed = discord.Embed(title="Check Check",description="that's not correct answer")
                await message.channel.send(embed=embed)
                return

            if user_res in result:
                user_res2 = result[user_res][0] # user_res2 = 아이템 명
                if user_res2 == "STUN":
                    
                    # 상대방 status = -1 로 업데이트
                    # stun 없애기
                    itemlists.updateitem(str(message.author),"STUN;")
                    return

                if user_res2 == "REDEMPTION":
                    
                    # 문제 안푸셨나요? = 상태가 0인지 확인
                        # step 사용
                        # redemption 없애기
                    itemlists.updateitem(str(message.author),"REDEMPTION;")
                    return

                if user_res2 == "SNAKE": #snake의 기준은 뭐지 문서봐도 모르겠
                    # 스네이크 없애기
                    itemlists.updateitem(str(message.author),"SNAKE;")
                    return

                '''
                if user_res2 == "STEP": # STEP SKIP
                    return
                if user_res2 == "CAFFEINE": #보스레이드
                    return
                if user_res2 == "REDBULL": #보스레이드
                    return
                if user_res2 == "BOMB": #보스레이드
                    return
                '''

            else:
                await message.channel.send("you don't have it. plz check your bag")
                return


            
        
client.run(os.environ['token'])
