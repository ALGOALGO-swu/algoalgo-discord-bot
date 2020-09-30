import pymysql
import os
import algoalgo_bj_crawling

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

def adduser(author, cmd):
    args = cmd.split()
    if author == "admin" and len(args) != 5:
        return "Usage : !adduser <name> <student_id> <baekjoon_id> <discord_id>"
    elif author != "admin" and len(args) != 4:
        return "Usage : !adduser <name> <student_id> <baekjoon_id>"
    # !adduser <이름> <학번> <백준 아이디>

    dc_id = author == "admin" if author else args[4]
    name = args[1]
    s_id = args[2]
    bj_id = args[3]
    bj_solved = algoalgo_bj_crawling.getBJSolved(bj_id)

    sql = "insert into member (discord_id, student_id, name, baekjoon_id, bj_solved) value (%s, %s, %s, %s, %s);"
    try:
        sql_update(sql, dc_id, s_id, name, bj_id, bj_solved)
    except Exception as ex:
        return f"[!] An error occurs while adding user({author}) into db....\n[INFO] error : {ex}"
    
    return f"[+] success adding user into db...{author}"

def showuserinfo(author):
    sql = f"select * from member where discord_id='{str(author)}'"

    try:
        sql_result = sql_exe(sql)
        print(sql_result)
        
        # status : 1, 2, 3에 맞는 값을 각각 문자열로 풀어서 출력
        # items : 아이템 보유 개수 정리해서 출력
        userinfo = f"""discord_id : {sql_result[0]['discord_id']}
        name : {sql_result[0]['name']}
        **- GAME INFO**
        status : {sql_result[0]['status']}
        your steps on today : {sql_result[0]['daily_steps']}
        your point : {sql_result[0]['point']}
        your location : {sql_result[0]['map_location']}
        items : {sql_result[0]['items']}
        **- BAEKJOON INFO**
        baekjoon id : {sql_result[0]['baekjoon_id']}
        Continuous Days of Mission : {sql_result[0]['bj_solv_contd']}
        """ 

        return f"[*] Successfully Inquires data about {author}", userinfo
    except Exception as ex:
        return f"[!] An error occurs while finding user({author}) in db....\n[INFO] error : {ex}", None
    


def truncate(cmd):
    args = cmd.split()
    table = args[1]

    if table == "achievement":
        return f"[!] ERROR : You can't truncate table {table}"

    sql = f"truncate table {table};"
    
    try:
        sql_update(sql)
    except Exception as ex:
        return f"[!] An error occurs while truncating table {table}....\n[INFO] error : {ex}"

    return f"[-] success truncating table .... {table}"

