import pymysql

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

pointinfo=""
def point_check(author):
    sql = f"select * from member where discord_id='{str(author)}'"
    try:
        sql_result = sql_exe(sql)
        pointinfo = f"""{sql_result[0]['point']}"""
        return f"[*] Successfully Inquires data about the feature of the {author}'s point'", pointinfo
    except Exception as ex:
        return f"[!] point check error!\n[INFO]: {ex}"

def setpoint(author):
    sql = f"update member set point = 10 where discord_id='{str(author)}'"
    try:
        sql_exe(sql)
        return f"[*] 테스트용 10 포인트세팅"
    except Exception as ex:
        return f"[!] setpoint error!\n[INFO]: {ex}"

ITEMS = ["STEP", "REDEMPTION", "SNAKE", "ASSASSIN", "STUN", "CAFFEINE", "REDBULL", "BOMB"]
PRICE = [3, 5, 10, 6, 6, 3, 5, 6]
def buy_item(author, cmd): #!buy_item <아이템> <개수>
    args = cmd.split()
    if len(args) != 3:
        return "Usage: !buyitem <item name> <number>"
    
    item = args[1]
    cnt = int(args[2])
    item_price = int(PRICE[ITEMS.index(item)])*cnt

    sql = f"select * from member where discord_id='{str(author)}'"
    sql_result = sql_exe(sql)
    pointinfo = f"""{sql_result[0]['point']}"""

    if item not in ITEMS:
        return "Please enter the item name correctly"
    
    if item_price > int(pointinfo):
        return "You don't have enough points"
    
    gogo=''
    for i in range(cnt):
        gogo+=item+';'
    
    sql = f"update member set items = CONCAT(items, (%s)) where discord_id='{str(author)}'"
    sql2 = f"update member set point = point-{item_price} where discord_id='{str(author)}'"
    try:
        sql_update(sql, gogo)
        sql_exe(sql2)
    except Exception as ex:
        return f"[!] buy item error!\n[INFO]: {ex}"
    return f"[+] success updating item into db: {author}\n구매 성공! {item_price} 포인트 차감되었습니다"
