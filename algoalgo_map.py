import pymysql
import os
import algoalgo_sql
import algoalgo_error

#     getPlayers() #해당 칸에 위치한 플레이어 
#     getItems()  #해당 칸에 위치한 아이템
#     getFloorType() #해당 칸이 어떤 칸인지. 문제 칸 or 사다리 or 뱀
# id : 칸 순서 
# feature: 칸 종류 :: 일반 칸 사다리 뱀  보스
# ahead_to : 사다리나 뱀일 경우 이동할 칸의 번호 

# 맵 설정
def setmap(cmd):
    args = cmd.split()
    if len(args) != 4:
        return "Usage : !set_map <id> <feature> <ahead_to>"
    # !set_map <칸 순서> <normal: 0, ladder: 1, snake: 2, boss: 3> <이동할 위치>

    id = args[1]
    feature = args[2]
    ahead_to = args[3]
   

    sql = "insert into map (id, feature, ahead_to) value (%s, %s, %s);"
    try:
        algoalgo_sql.sql_update(sql, int(id), int(feature), int(ahead_to))
    except Exception as ex:
        return f"[!] An error occurs while adding map data into db....\n[INFO] error : {ex}"
    
    return f"[+] success adding map data into db..."

# nowLoc의 속성 반환
#<normal: 0, ladder: 1, snake: 2, boss: 3> 
def getLocType(cmd):
    args = cmd.split()
    nowLoc = args[1]

    sql = f"select * from map where id='{nowLoc}'"

    try:
        sql_result = algoalgo_sql.sql_exe(sql)
        print(sql_result)
     
        if sql_result[0]['feature'] == 0 :
            LocFeatureInfo = "**NOMAL**🦶"
        
        if sql_result[0]['feature'] == 1 :
            LocFeatureInfo = "**LADDER**👣"

        if sql_result[0]['feature'] == 2 :
            LocFeatureInfo = "**SNAKE**🐍"
              
        if sql_result[0]['feature'] == 3 :
            LocFeatureInfo = "**BOSS**🧟‍♀️"
        
        
        
        return f"[*] Successfully Inquires data about the feature of the {nowLoc} location on the map", LocFeatureInfo, nowLoc
    except Exception as ex:
        return f"[!] An error occurs while finding the feature of the {nowLoc} location on the map in db....\n[INFO] error : {ex}"
    

# nowLoc에 있는 플레이어들의 이름 출력
def getPlayers(cmd):
    args = cmd.split()
    nowLoc = args[1]

    sql = f"select name from member where map_location='{nowLoc}'"

    try:
        sql_result = algoalgo_sql.sql_exe(sql)
        print(sql_result)
        
        Locinfo = ""

        for person in sql_result:
            Locinfo += person['name'] +"\n"

        return f"[*] Successfully Inquires data about the users in the {nowLoc} location on the map", Locinfo , nowLoc
    except Exception as ex:
        return f"[!] An error occurs while finding the users in the {nowLoc} location on the map in db....\n[INFO] error : {ex}"
    

# player's loc 반환
def showmap(author):
    sql = f"select map_location from member where discord_id='{str(author)}'"

    try:
        sql_result = algoalgo_sql.sql_exe(sql)
        print(sql_result)
     
        Locinfo = sql_result[0]['map_location']

        return f"[*] Successfully Inquires data about **{author}** 's location on the map", Locinfo
    except Exception as ex:
        return f"[!] An error occurs while finding **{author}** 's location on the map in db....\n[INFO] error : {ex}"


# SNAKE
def snake(discord_id):
    #STEP 6-2 는 메세지로 알려주기
    sql = f"select * from member where discord_id='{str(discord_id)}'"
    
    try:
        sql_result = algoalgo_sql.sql_exe(sql)

        map_sql = f"select * from map where id='{sql_result[0]['map_location']}'"
        map_sql_result = algoalgo_sql.sql_exe(map_sql)

        #STEP 6-2 는 메세지로 알려주기

        map_location_sql2 = f"update member set map_location ='{map_sql_result[0]['ahead_to']}' where discord_id='{str(discord_id)}'"
        algoalgo_sql.sql_update(map_location_sql2)
        return f"[*] Successfully updataed data about **{discord_id}** 's location on the snake map"


    except Exception as ex:
        return f"[!] An error occurs while finding **{discord_id}** 's location on the map in db....\n[INFO] error : {ex}"







# STEP
def step(discord_id):
    try:
        sql = f"select * from member where discord_id='{str(discord_id)}'"
        sql_result = algoalgo_sql.sql_exe(sql)

        #STEP-2
        daily_step_sql = f"update member set daily_steps ='{sql_result[0]['daily_steps'] + 1}' where discord_id='{str(discord_id)}'"
        algoalgo_sql.sql_update(daily_step_sql)

        #STEP-3
        if sql_result[0]['status'] == 1:

            #STEP-4
            map_location_sql = f"update member set map_location ='{sql_result[0]['map_location'] + 1}' where discord_id='{str(discord_id)}'"
            algoalgo_sql.sql_update(map_location_sql)

            #STEP-5
            map_sql = f"select * from map where id='{int(sql_result[0]['map_location'])+1}'"
            map_sql_result = algoalgo_sql.sql_exe(map_sql)

            if map_sql_result[0]['feature'] == 1 :
                map_location_sql2 = f"update member set map_location ='{map_sql_result[0]['ahead_to']}' where discord_id='{str(discord_id)}'"
                algoalgo_sql.sql_update(map_location_sql2)
                return f"[*] Successfully updated data about **{discord_id}** 's location on the map", map_sql_result[0]['feature'], 3 - (sql_result[0]['daily_steps'] + 1)

            # if map_sql_result[0]['feature'] == 2 :
            #     # LocFeatureInfo = "**SNAKE**🐍"
            #     return f"[*] Successfully updated data about **{discord_id}** 's location on the map", map_sql_result[0]['feature'], 3 - (sql_result[0]['daily_steps'] + 1)

            # if map_sql_result[0]['feature'] == 3 :
            #     # LocFeatureInfo = "**BOSS**🧟‍♀️"
            #     return f"[*] Successfully updated data about **{discord_id}** 's location on the map", map_sql_result[0]['feature'], 3 - (sql_result[0]['daily_steps'] + 1)

            return f"[*] Successfully updated data about **{discord_id}** 's location on the map", map_sql_result[0]['feature'], 3 - (sql_result[0]['daily_steps'] + 1)


        else:
            # raise 해야함
            return f"[*] 문제를 푸셔야합니다.", 0, 0

    except Exception as ex:
        #raise 해야함 
        return f"[!] An error occurs while finding **{discord_id}** 's location on the map in db....\n[INFO] error : {ex}",0,0


#step - initialize status
def init_status(author):
    sql = "update member set status = 0 where discord_id = %s;"

    try:
        algoalgo_sql.sql_update(sql, str(author))
        print(f"[*] Successfully init status data about {author}")

    except Exception as ex:
        e_msg = f"[!] An error occurs while initializing status about {author} in db....\n[INFO] error : {ex}"
        raise algoalgo_error.UserDefinedException(e_msg)



