import pymysql
import os
import algoalgo_sql


pointinfo=""
def point_check(author):
    sql = f"select * from member where discord_id='{str(author)}'"
    try:
        sql_result = algoalgo_sql.sql_exe(sql)
        pointinfo = f"""{sql_result[0]['point']}"""
        return f"[*] Successfully Inquires data about the feature of the {author}'s point'", pointinfo
    except Exception as ex:
        return f"[!] point check error!\n[INFO]: {ex}"

def setpoint(author):
    sql = f"update member set point = 10 where discord_id='{str(author)}'"
    try:
        algoalgo_sql.sql_exe(sql)
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
    sql_result = algoalgo_sql.sql_exe(sql)
    pointinfo = f"""{sql_result[0]['point']}"""

    if item not in ITEMS:
        return "Please enter the item name correctly"
    
    if item_price > int(pointinfo):
        return "You don't have enough points"
    
    gogo=''
    for i in range(cnt):
        gogo+=item+';'
    
    sql = f"update member set items = CONCAT_WS(';', items, %s) where discord_id='{str(author)}'"
    sql2 = f"update member set point = point-{item_price} where discord_id='{str(author)}'"
    try:
        algoalgo_sql.sql_update(sql, gogo)
        algoalgo_sql.sql_update(sql2)
    except Exception as ex:
        return f"[!] buy item error!\n[INFO]: {ex}"
    return f"[+] success updating item into db: {author}\n구매 성공! {item_price} 포인트 차감되었습니다"
