import pymysql
import unicodedata

# select * ->

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
        cursor.execute(query, args)

        result = cursor.fetchall()

        db_conn.commit()
        db_conn.close()

        return result

    except Exception as ex:
        raise ex

def fill_str_with_space(input_s="", max_size=27, fill_char=" "):
    l = 0
    for c in input_s:
        if unicodedata.east_asian_width(c) in ['F', 'W']:
            l+=2
        else:
            l+=1
    return input_s+fill_char*(max_size-l)

def addpoint(cmd):
    args = cmd.split(' ')
    if len(args) != 3:
        return "Usage : !addpoint <archivement id> <student_id or discord_id>"
    # !addpoint <업적 번호> <학번 또는 디스코드 닉네임>

    # 권한 확인: 추가 예정

    # 업적 정보 확인
    result = sql_exe("SELECT points, achive_name FROM achievement WHERE id = %s", args[1])[0]
    point = result['points']
    achname = result['achive_name']

    # 포인트 업데이트
    if args[2].find('#') == -1: # 학번 입력시
        sql = "UPDATE member SET point = point+%s WHERE student_id = %s;"
        sql_update(sql, point, args[2])
        name = sql_exe("SELECT discord_id FROM member WHERE student_id = %s", args[2])[0]['discord_id']
    else: # 디스코드 닉네임 입력시
        name = args[2]
        sql = "UPDATE member SET point = point+%s WHERE discord_id = %s;"
        sql_update(sql, point, name)

    return f"Mission Accomplished: {achname} by {name}"

def refresh():
    sql_update("UPDATE member SET daily_steps = 0")
    sql_update("UPDATE member SET status = 0 WHERE status = -1")

    sids = sql_exe("SELECT student_id, bj_solv_contd FROM member WHERE bj_solv_contd IN (5, 14, 30)")
    for sid in sids:
        # 달성 업적 확인
        if sid['bj_solv_contd'] == 5:
            aid = 12
        elif sid['bj_solv_contd'] == 14:
            aid = 13
        else:
            aid = 14

        addpoint(f"!addpoint {aid} {sid['student_id']}")

    return f"Refresh Done"

def list_achievement():
    achlist = sql_exe("SELECT description, points FROM achievement WHERE is_hidden = 0")
    printlist = []
    for ach in achlist:
        printlist.append(f"{fill_str_with_space(ach['description'])}{ach['points']} 포인트")
    return "\n".join(printlist)

"""printlist = []
    printlist.append("| Title | Points |")
    printlist.append("| :-----: | ----: |")
    for ach in achlist:
        printlist.append(f"| {ach['description']} | {ach['points']} |")"""