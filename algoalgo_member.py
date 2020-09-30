import pymysql
import unicodedata
import requests
from bs4 import BeautifulSoup
from random import randint

# select * ->

def sql_update(query, *args):
    db_conn = pymysql.connect(
        user='',
        passwd='',
        host='',
        db='',
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


def sql_update_many(query, *args):
    db_conn = pymysql.connect(
        user='',
        passwd='',
        host='',
        db='',
        charset='utf8'
    )

    cursor = db_conn.cursor(pymysql.cursors.DictCursor)
    try:
        if args == None:
            cursor.executemany(query)
        else:
            print(query, args)
            cursor.executemany(query, args[0])

        db_conn.commit()
        db_conn.close()

    except Exception as ex:
        raise ex


def sql_exe(query, *args):
    db_conn = pymysql.connect(
        user='',
        passwd='',
        host='',
        db='',
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
        userinfo = f"""
        discord_id : {sql_result[0]['discord_id']}
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
        return f"[!] An error occurs while finding user({author}) in db....\n[INFO] error : {ex}"


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
    sql_update("UPDATE member SET bj_solv_contd = bj_solv_contd+1 WHERE bj_today <> 0")
    sql_update("UPDATE member SET bj_solv_contd = 0 WHERE bj_today = 0")
    sql_update("UPDATE member SET bj_today = 0")
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


def problem_rank_update():
    def crawler(url):
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        text = soup.select('a.gLFkLK > span')
        if len(text) == 0:
            return 0
        else:
            qids = []
            for item in text:
                qids.append(int(item.text))
            return qids

    def get_problem_list(rank):
        problemsbyrank = []
        page = 1
        while page != 0:
            ids = crawler(f'https://solved.ac/problems/level/{rank}?sort=id&direction=ascending&page={page}')
            if ids == 0:
                page = 0
            else:
                problemsbyrank += ids
                page += 1
        print(len(problemsbyrank))
        return problemsbyrank

    def save_problem_list(rank):
        sql = "insert into solved_rank (id, rank) values (%s, %s);"
        vals = []
        for problem in get_problem_list(rank):
            vals.append([problem, rank])
        try:
            sql_update_many(sql, vals)
        except Exception as ex:
            print(ex)
            return f"[!] An error occurs while updating problem ranks into db....\n[INFO] error : {ex}"

    print("starting update")
    for rank in range(1, 31):
        save_problem_list(rank)
        print(rank)

    print('done')
    return


def get_solved(bojid):
    soup = BeautifulSoup(requests.get(f'https://www.acmicpc.net/user/{bojid}').text, 'html.parser')
    text = soup.select_one('div.panel-body')
    solved = text.text.split('\n')[1:-1:2]
    return solved


def random_bj(author, cmd):
    bojid = sql_exe("SELECT baekjoon_id FROM member WHERE discord_id = %s", author)[0]['baekjoon_id']
    solved = get_solved(bojid)

    args = cmd.split()
    if len(args) != 2:
        return "Usage : !random_bj <tier>"
    tier = args[1]

    if tier == 'bronze':
        startfrom = 1
    elif tier == 'silver':
        startfrom = 6
    elif tier == 'gold':
        startfrom = 11
    elif tier == 'platinum':
        startfrom = 16
    elif tier == 'diamond':
        startfrom = 21
    elif tier == 'ruby':
        startfrom = 26
    else:
        return "There is no such tier in solved.ac."

    sql = "SELECT id FROM solved_rank WHERE rank >= %s and rank < %s;"
    result = sql_exe(sql, startfrom, startfrom+5)
    candidate = []
    for item in result:
        candidate.append(item['id'])
    print(candidate)

    while True:
        rbj = candidate[randint(0, len(candidate))]
        if rbj not in solved:
            break;
    return f'https://www.acmicpc.net/problem/{rbj}'


def daily_baekjoon(author, cmd):
    args = cmd.split()
    if len(args) != 2:
        return "Usage : !daily_baekjoon <Problem id>"
    pid = args[1]
    solvedlist = sql_exe("SELECT bj_solved FROM member WHERE discord_id = %s", author)[0]['bj_solved']
    if pid in solvedlist.split(';')[:-1]:
        return "이미 인증된 문제입니다."
    if pid not in get_solved(sql_exe("SELECT baekjoon_id FROM member WHERE discord_id = %s", author)[0]['baekjoon_id']):
        return "문제를 풀지 않았습니다."
    solvedlist += (str(pid) + ';')
    sql_update("UPDATE member SET bj_solved = %s WHERE discord_id = %s", solvedlist, author)
    addpoint(f"!addpoint 11 {author}")
    sql_update("UPDATE member SET bj_today = 1 WHERE discord_id = %s", author)
    return "인증이 완료되었습니다."

def unlock(author):
    memberinfo = sql_exe("SELECT status, map_location, baekjoon_id, bj_solved FROM member WHERE discord_id = %s", author)[0]
    if memberinfo['status'] == 1:
        return "이미 해제되었습니다. 다음 칸으로 이동해주세요."
    if memberinfo['status'] == -1:
        return "stun이 걸려있습니다. 내일 00:00 이후 다시 진행해주세요."
    if memberinfo['status'] == 0:
        pid = sql_exe("SELECT baekjoon_no FROM map WHERE id = %s", memberinfo['map_location'])[0]['baekjoon_no']
        print(pid)
        if pid in get_solved(memberinfo['baekjoon_id']):
            sql_update("UPDATE member SET status = 1 WHERE baekjoon_id = %s", memberinfo['baekjoon_id'])
            if pid not in memberinfo['bj_solved'].split(';')[:-1]:
                memberinfo['bj_solved'] += (str(pid) + ';')
            return "해제되었습니다."
        else:
            print(get_solved(memberinfo['baekjoon_id']))
            return "문제를 풀지 않으셨습니다."
    else:
        return "에러가 발생하였습니다."