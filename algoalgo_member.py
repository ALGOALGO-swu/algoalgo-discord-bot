import pymysql

def sql_exe(query, *args):
    db_conn = pymysql.connect(
        user='staff', 
        passwd='algoalgo-staff', 
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

def adduser(author, cmd):
    args = cmd.split()
    if len(args) != 4:
        return "Usage : !adduser <name> <student_id> <baekjoon_id>"
    # !adduser <이름> <학번> <백준 아이디>

    dc_id = author
    name = args[1]
    s_id = args[2]
    bj_id = args[3]
    bj_solved = "sample;sample1;sample2;"

    sql = "insert into member (discord_id, student_id, name, baekjoon_id, bj_solved) value (%s, %s, %s, %s, %s);"
    try:
        sql_result = sql_exe(sql, dc_id, s_id, name, bj_id, bj_solved)
    except Exception as ex:
        return f"[!] An error occurs while adding user({author}) into db....\n[INFO] error : {ex}"
    
    return f"[+] success adding user into db...{author}"

def showuserinfo(author):
    pass

def truncate(cmd):
    args = cmd.split()
    table = args[1]

    if table == "achievement":
        return f"[!] ERROR : You can't truncate table {table}"

    return "testing..."

    sql = f"truncate table {table};"
    
    try:
        sql_result = sql_exe(sql)
    except Exception as ex:
        return f"[!] An error occurs while truncating table {table}....\n[INFO] error : {ex}"

    return f"[-] success truncating table .... {table}"

