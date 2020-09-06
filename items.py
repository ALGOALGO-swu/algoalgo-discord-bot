import pymysql

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
        """
        return f"{author}의 daily_stops check 성공", dailyinfo
    except Exception as ex:
        return f"error!\n[무슨에러?]: {ex}"
