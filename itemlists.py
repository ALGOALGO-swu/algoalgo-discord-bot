import pymysql
import os
from collections import Counter

def sql_update(query, *args):
    db_conn = pymysql.connect(
        user='staff', 
        passwd=os.environ['db_pass'], 
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
        passwd=os.environ['db_pass'], 
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

def testupdate(author):
    sql = f"update member set items = 'ASSASSIN;STUN;STEP;STEP;ASSASSIN;SNAKE;SNAKE;REDEMPTION;REDEMPTION;STUN;' where discord_id='{str(author)}'"
    #sql = f"select items from member where discord_id='{str(author)}'"
    try:
        result=sql_exe(sql)
        #return "[+]테스트 10점 넣어줌"
        return f"[+]db item update '{author}'"
    except Exception as ex:
        return "[!]db x."

# 사용자가 실제 멤버인지 확인
def checkMember(person):
    sql = f"select name from member where discord_id='{str(person)}'"
    try:
        sql_result=sql_exe(sql)
        #print(sql_result)
        return sql_result
    except Exception as ex:
        return f"[!] error finding '{str(person)}'"

# 사용자 stat -1로 설정하기
def setStun(person):
    sql = f"update member set status = -1 where discord_id='{str(person)}'"
    try:
        sql_exe(sql)
        print("[+] success stun")
        return f"[+] success stun '{str(person)}'"
    except Exception as ex:
        return f"[!] error stun '{str(person)}'"

# redemption 사용하여 stat 1로 설정하기
def setRedemption(author):
    sql = f"update member set status = 1 where discord_id='{str(author)}'"
    try:
        sql_exe(sql)
        print("[+] success Redemption")
        return f"[+] success Redemption '{str(author)}'"
    except Exception as ex:
        return f"[!] error Redemption '{str(author)}'"

# 아이템 사용 후 테이블 업데이트
def updateitem(author,item):
    sql = f"select items from member where discord_id='{str(author)}'"
    try:
        sql_result=sql_exe(sql)
        #print(sql_result)
        sql_result2=sql_result[0]['items'].replace(item,"",1)
        #print(sql_result2)
    except Exception as ex:
        return f"[!] error select '{str(author)}' DB"

    sql2 = f"update member set items ='{str(sql_result2)}' where discord_id='{str(author)}'"    
    try:
        sql_exe(sql2)
    except Exception as ex:
        return f"[!] error update '{str(author)}' DB"
    
    return f"[+] success use item '{author}', '{item}'" 

# assassin으로 사용자 뒤로 옮기기
def setAssassin(person):
    sql = f"select map_location from member where discord_id='{str(person)}'"
    try:
        sql_result=sql_exe(sql)
    except Exception as ex:
        return f"[!] error select '{str(person)}' DB"

    sql2 = f"update member set map_location = {int(sql_result[0]['map_location'])-1} where discord_id='{str(person)}'"    
    try:
        sql_exe(sql2)
    except Exception as ex:
        return f"[!] error update '{str(person)}' DB"
    return f"[+] success use item '{person}', Assasin" 

# 소유한 아이템 리턴
def useitem(author):
    sql = f"select items from member where discord_id='{str(author)}'"
    try:
        sql_result=str(sql_exe(sql))
        # 인덱스. 아이템명 : 소유 개수 형식의 리스트 출력해야함
        itemlist=sql_result.split(";") # 중복있는 아이템목록
        count = Counter(itemlist) # 유저의 아이템 종류 수
       
        # 인벤토리가 비었다.
        if len(count) == 1:
            return 0

        # print(shop&itemlist) # showuserinfo 에서 나오는 아이템 목록 출력?
        shop={"STEP", "REDEMPTION", "SNAKE", "ASSASSIN", "STUN", "CAFFEINE", "REDBULL", "BOMB"}
        itemlists = list(shop&set(itemlist)) # 중복없는 아이템 목록

        # 인덱스 및 아이템 갯수 넣기
        index = len(count)-1 #유저가 가진 아이템 가짓수
        item_dic={} #딕셔너리: 유저 아이템 인덱스,[아이템명,가진수] 
        
        ''' 유저가 가진 아이템 목록 출력'''
        for id,it in zip(range(index),itemlists):
            #print(id+1,".",it,":",count[it],"개") # 인덱스. 아이템명:아이템갯수 개 
            item_dic[id]=[it,count[it]] #딕셔너리로 묶어놓음
            #print(id+1,".",item_dic[id][0],":",item_dic[id][1],"개")

        return item_dic #아이템 인덱스,[아이템명,가진수] 반환

    except Exception as ex:
        return "[!] error finding your info: ", ex

