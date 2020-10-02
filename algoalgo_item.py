import pymysql
import os
from collections import Counter
import algoalgo_sql
import algoalgo_error

def testupdate(author):
    sql = f"update member set items = 'ASSASSIN;STUN;STEP;STEP;ASSASSIN;SNAKE;SNAKE;REDEMPTION;REDEMPTION;STUN;' where discord_id='{str(author)}'"
    #sql = f"select items from member where discord_id='{str(author)}'"
    try:
        result=algoalgo_sql.sql_exe(sql)
        #return "[+]테스트 10점 넣어줌"
        return f"[+]db item update '{author}'"
    except Exception as ex:
        return "[!]db x."

# 사용자가 실제 멤버인지 확인
def checkMember(person):
    sql = f"select name from member where discord_id='{str(person)}'"
    try:
        sql_result=algoalgo_sql.sql_exe(sql)
        #print(sql_result)
        return sql_result
    except Exception as ex:
        raise f"[!] error finding '{str(person)}'"

# 사용자 stat -1로 설정하기
def setStun(person):
    sql = f"update member set status = -1 where discord_id='{str(person)}'"
    try:
        algoalgo_sql.sql_update(sql)
        print("[+] success stun")
        return f"[+] success stun '{str(person)}'"
    except Exception as ex:
        raise f"[!] error stun '{str(person)}'"

# redemption 사용하여 stat 1로 설정하기
def setRedemption(author):
    sql = f"update member set status = 1 where discord_id='{str(author)}'"
    try:
        algoalgo_sql.sql_update(sql)
        print("[+] success Redemption")
        return f"[+] success Redemption '{str(author)}'"
    except Exception as ex:
        raise f"[!] error Redemption '{str(author)}'"

# 아이템 사용 후 테이블 업데이트
def updateitem(author,item):
    sql = f"select items from member where discord_id='{str(author)}'"
    try:
        sql_result=algoalgo_sql.sql_exe(sql)
        
        sql_result2=sql_result[0]['items'].replace(item,"",1)

    except Exception as ex:
        raise f"[!] error select '{str(author)}' DB"

    sql2 = f"update member set items ='{str(sql_result2)}' where discord_id='{str(author)}'"    
    try:
        algoalgo_sql.sql_update(sql2)
    except Exception as ex:
        raise f"[!] error update '{str(author)}' DB"
    
    return f"[+] success use item '{author}', '{item}'" 

# assassin으로 사용자 뒤로 옮기기
def setAssassin(person):
    sql = f"select map_location from member where discord_id='{str(person)}'"
    try:
        sql_result=algoalgo_sql.sql_exe(sql)
    except Exception as ex:
        return f"[!] error select '{str(person)}' DB"

    sql2 = f"update member set map_location = {int(sql_result[0]['map_location'])-1} where discord_id='{str(person)}'"    
    try:
        algoalgo_sql.sql_update(sql2)
    except Exception as ex:
        raise f"[!] error update '{str(person)}' DB"
    return f"[+] success use item '{person}', Assasin" 

# 소유한 아이템 리턴
def useitem(author):
    sql = f"select items from member where discord_id='{str(author)}'"
    try:
        sql_result=algoalgo_sql.sql_exe(sql)
        item_dir = show_items(sql_result[0]['items'])
        # 인덱스. 아이템명 : 소유 개수 형식의 리스트 출력해야함
        itemlist=sql_result[0]['items'].split(";") # 중복있는 아이템목록
        count = Counter(itemlist) # 유저의 아이템 종류 수
       
        # 인벤토리가 비었다.
        if len(count) == 1:
            return 0

        return item_dir # 아이템 보유 현황에 대한 dict 반환

    except Exception as ex:
        e_msg =  "[!] error finding your info: "
        raise algoalgo_error.UserDefinedException(e_msg)



def show_items(items_list):
    try:
        item_dir = {"STEP" : 0,
        "SNAKE" : 0,
        "STUN" : 0,
        "ASSASSIN" : 0,
        "REDEMPTION" : 0,
        "CAFFEINE" : 0,
        "BOMB" : 0,
        "RED BULL" : 0
        }
        if items_list != None:    
            items_list = items_list.rstrip(';')
            items = items_list.split(';')
            for item in items:
                if len(item) == 0:
                    continue
                item_dir[item] += 1
        return item_dir
    except Exception as ex:
        raise ex