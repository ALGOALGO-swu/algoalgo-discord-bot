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
        passwd=os.environ['token'], 
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
# 사용자가 실제 멤버인지 확인
def checkMember(person):
    sql = "select name from member where discord_id='{person}'"
    try:
        sql_result=sql_exe(sql)
        return "[*] success access '{person}'",True
    except Exception as ex:
        return "[!] error finding '{person}'",False

# 아이템 사용 후 테이블 업데이트
def updateitem(author,item):
    sql = "select items from member where discord_id='{author}'"
    sql_result=sql_exe(sql)
    sql_result=sql_result.replace(item,"",1)
    sql2 = "update member set items ='{sql_result}' where discord_id='{author}'"
    sql_update(sql2)
    return "[+] success use item '{author}', '{item}'" 

# 소유한 아이템 출력
def useitem(author):
    sql = f"select items from member where discord_id='{str(author)}'"
    try:
        sql_result=sql_exe(sql)
        # 인덱스. 아이템명 : 소유 개수 형식의 리스트 출력해야함
        itemlist=sql_result.split(";") # 중복있는 아이템목록
        count = Counter(itemlist) # 유저의 아이템 종류 수
        
        try:

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
               print(id+1,".",item_dic[id][0],":",item_dic[id][1],"개")
            return "[*] success print itemlist {author}", item_dic #아이템 인덱스,[아이템명,가진수] 반환
            
        except Exception as ex:
            return "[!] can not access db", ex

    except Exception as ex:
        return "[!] error finding your info: ", ex

