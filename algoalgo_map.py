import pymysql
import os

def sql_update(query, *args):
    db_conn = pymysql.connect(
        user='staff', 
        passwd=os.environ["db"], 
        host='34.64.120.154', 
        db='algoalgo', 
        charset='utf8'
    )   

    cursor = db_conn.cursor(pymysql.cursors.DictCursor)
    try:
        if args == None:
            cursor.execute(query)
        else:
            cursor.execute(query, args)

        db_conn.commit()
        db_conn.close()
    
    except Exception as ex:
        raise ex

def sql_exe(query):
    db_conn = pymysql.connect(
        user='staff', 
        passwd=os.environ["db"], 
        host='34.64.120.154', 
        db='algoalgo', 
        charset='utf8'
    )   

    cursor = db_conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute(query)

        result = cursor.fetchall()            

        db_conn.commit()
        db_conn.close()

        return result 
    
    except Exception as ex:
        raise ex

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
        sql_update(sql, int(id), int(feature), int(ahead_to))
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
        sql_result = sql_exe(sql)
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

    sql = f"select discord_id from member where map_location='{nowLoc}'"

    try:
        sql_result = sql_exe(sql)
        print(sql_result)
        
        Locinfo = ""

        for person in sql_result:
            Locinfo += person
            # Locinfo += person['discord_id'] +"\n"

        return f"[*] Successfully Inquires data about the users in the {nowLoc} location on the map", Locinfo , nowLoc
    except Exception as ex:
        return f"[!] An error occurs while finding the users in the {nowLoc} location on the map in db....\n[INFO] error : {ex}"
    

# player's loc 반환
def showmap(author):
    sql = f"select map_location from member where discord_id='{str(author)}'"

    try:
        sql_result = sql_exe(sql)
        print(sql_result)
     
        Locinfo = sql_result[0]['map_location']

        return f"[*] Successfully Inquires data about **{author}** 's location on the map", Locinfo
    except Exception as ex:
        return f"[!] An error occurs while finding **{author}** 's location on the map in db....\n[INFO] error : {ex}"
   




# # 위치 이동 함수
# def shopstep(author, cmd):
#     args = cmd.split()
#     if len(args) != 4:
#         return "Usage : !shop_step <name> <student_id> <next_loc>"
#     # !shop_step <이름> <학번> <이동할 위치>

#     dc_id = author
#     name = args[1]
#     s_id = args[2]
#     next_loc = args[3]
   

    # sql = "insert into member (discord_id, student_id, name, baekjoon_id, bj_solved) value (%s, %s, %s, %s, %s);"
    # try:
    #     sql_update(sql, dc_id, s_id, name, bj_id, bj_solved)
    # except Exception as ex:
    #     return f"[!] An error occurs while adding user({author}) into db....\n[INFO] error : {ex}"
    
    # return f"[+] success adding user into db...{author}"