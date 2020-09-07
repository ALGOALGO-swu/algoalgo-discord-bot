import pymysql

def sql_update(query, *args):
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

def sql_exe(query):
    db_conn = pymysql.connect(
        user='staff', 
        passwd='algoalgo-staff', 
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

def step_check(author):
    sql = f"select * from member where discord_id='{str(author)}'"
    try:
        sql_result = sql_exe(sql)
        print(sql_result)
        dailyinfo = f"""
        오늘 남은 steps : {sql_result[0]['daily_steps']}
        남은 member point : {sql_result[0]['point']}
        """
        return f"{author}의 daily_stops check 성공", dailyinfo
    except Exception as ex:
        return f"error!\n[무슨에러?]: {ex}"

ITEMS = ["STEP", "REDEMPTION", "SNAKE", "ASSASSIN", "STUN", "CAFFEINE", "REDBULL", "BOMB"]
def buy_item(author, cmd): #!buy_item <아이템> <개수>
    args = cmd.split()
    if len(args) != 3:
        return "!buyitem <아이템> <개수> 형식에 맞춰주세요"

    item = args[1]
    cnt = args[2]

    if item not in ITEMS:
        return "아이템 이름을 똑바로 입력해 주세요"
    
    gogo=''
    for i in range(int(cnt)):
        gogo+=item+';'

    sql = f"update member set items = (%s) where discord_id='{str(author)}'"
    try:
        sql_update(sql, gogo)
    except Exception as ex:
        return f"error!\n[무슨에러?]: {ex}"
    return f"{author}의 {item} 아이템 {cnt}개 구매 완료"
