import unicodedata
import requests
from bs4 import BeautifulSoup
from random import randint

import algoalgo_bj_crawling
import algoalgo_sql


def adduser(author, cmd):
    args = cmd.split()
    if author == "admin" and len(args) != 5:
        return "[!] Usage : !adduser <name> <student_id> <baekjoon_id> <discord_id>"
    elif author != "admin" and len(args) != 4:
        return "[!] Usage : !adduser <name> <student_id> <baekjoon_id>"
    # !adduser <이름> <학번> <백준 아이디>

    dc_id = author if author != "admin" else args[4]
    name = args[1]
    s_id = args[2]
    bj_id = args[3]
    bj_solved = algoalgo_bj_crawling.getBJSolved(bj_id)

    sql = "insert into member (discord_id, student_id, name, baekjoon_id, bj_solved) value (%s, %s, %s, %s, %s);"
    try:
        algoalgo_sql.sql_update(sql, dc_id, s_id, name, bj_id, bj_solved)
    except Exception as ex:
        return f"[!] An error occurs while adding user({author}) into db....\n[INFO] error : {ex}"

    return f"[+] success adding user into db...{author}"


def showuserinfo(author):
    sql = f"select * from member where discord_id='{str(author)}';"

    try:
        sql_result = algoalgo_sql.sql_exe(sql)

        item_dir = show_items(sql_result[0]['items'])
        # status : 1, 2, 3에 맞는 값을 각각 문자열로 풀어서 출력
        # items : 아이템 보유 개수 정리해서 출력

        userinfo = f"""discord_id : {sql_result[0]['discord_id']}
        name : {sql_result[0]['name']}
        **- GAME INFO**
        status : {sql_result[0]['status']}
        your steps on today : {sql_result[0]['daily_steps']}
        your point : {sql_result[0]['point']}
        your location : {sql_result[0]['map_location']}
        **- items**
        ```
STEP        | {item_dir['STEP']}
SNAKE       | {item_dir['SNAKE']}
STUN        | {item_dir['STUN']}
ASSASSIN    | {item_dir['ASSASSIN']}
REDEMPTION  | {item_dir['REDEMPTION']} ```
        **- BAEKJOON INFO**
        baekjoon id : {sql_result[0]['baekjoon_id']}
        Continuous Days of Mission : {sql_result[0]['bj_solv_contd']}
        """
        return f"[*] Successfully Inquires data about {author}", userinfo
    except Exception as ex:
        return f"[!] An error occurs while finding user({author}) in db....\n[INFO] error : {ex}", None


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
        return "[!] Usage : !addpoint <archivement id> <student_id or discord_id>"
    # !addpoint <업적 번호> <학번 또는 디스코드 닉네임>

    # 업적 정보 확인
    try:
        result = algoalgo_sql.sql_exe("SELECT points, achive_name FROM achievement WHERE id = %s", args[1])[0]
    except Exception as ex:
        return f"[!] An error occurs while check the db....\n[INFO] error : {ex}"

    point = result['points']
    achname = result['achive_name']

    # 포인트 업데이트
    if args[2].find('#') == -1: # 학번 입력시
        sql = "UPDATE member SET point = point+%s WHERE student_id = %s;"
        try:
            algoalgo_sql.sql_update(sql, point, args[2])
            name = algoalgo_sql.sql_exe("SELECT discord_id FROM member WHERE student_id = %s", args[2])[0]['discord_id']
        except Exception as ex:
            return f"[!] An error occurs while update the point into db....\n[INFO] error : {ex}"

    else: # 디스코드 닉네임 입력시
        name = args[2]
        try:
            sql = "UPDATE member SET point = point+%s WHERE discord_id = %s;"
            algoalgo_sql.sql_update(sql, point, name)
        except Exception as ex:
            return f"[!] An error occurs while update the point into db....\n[INFO] error : {ex}"

    return f"[+] Mission Accomplished: {achname} by {name}"


def refresh():
    try:
        algoalgo_sql.sql_update("UPDATE member SET daily_steps = 0")  # 일일 문제풀이 가능 횟수
        algoalgo_sql.sql_update("UPDATE member SET status = 0 WHERE status = -1")  # Stun 초기화

        # 연속 업적 달성 확인
        algoalgo_sql.sql_update("UPDATE member SET bj_solv_contd = bj_solv_contd+1 WHERE bj_today <> 0")
        algoalgo_sql.sql_update("UPDATE member SET bj_solv_contd = 0 WHERE bj_today = 0")
        algoalgo_sql.sql_update("UPDATE member SET bj_today = 0")

        # 연속 업적 달성자 업적 반영
        sids = algoalgo_sql.sql_exe("SELECT student_id, bj_solv_contd FROM member WHERE bj_solv_contd IN (5, 14, 30)")
        for sid in sids:
            # 달성 업적 확인
            if sid['bj_solv_contd'] == 5:
                aid = 12
            elif sid['bj_solv_contd'] == 14:
                aid = 13
            else:
                aid = 14

            addpoint(f"!addpoint {aid} {sid['student_id']}")
    except Exception as ex:
        return f"[!] An error occurs while refresh db....\n[INFO] error : {ex}"

    print('refresh done')
    return f"[+] Refresh Done"


def list_achievement():
    # DB에서 업적 목록 확인
    try:
        achlist = algoalgo_sql.sql_exe("SELECT description, points FROM achievement WHERE is_hidden = 0")
    except Exception as ex:
        return f"[!] An error occurs while check db....\n[INFO] error : {ex}"

    # 업적 목록 만들기
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
    # solved.ac 크롤러
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

    # 해당 랭크 문제 목록 가져오기
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
        return problemsbyrank

    # 해당 랭크 문제 목록 DB 저장
    def save_problem_list(rank):
        sql = "insert into solved_rank (id, rank) values (%s, %s);"
        vals = []
        for problem in get_problem_list(rank):
            vals.append([problem, rank])
        try:
            algoalgo_sql.sql_update_many(sql, vals)
        except Exception as ex:
            print(ex)
            return f"[!] An error occurs while updating problem ranks into db....\n[INFO] error : {ex}"

    # Bronze 5 ~ Ruby 1 업데이트
    print("starting update")
    for rank in range(1, 31):
        save_problem_list(rank)
        print(rank)
    print('done')
    return f"[+] Successfully Updated Rank & Problem Table"


# BOJ 푼 문제 목록 크롤러
def get_solved(bojid):
    soup = BeautifulSoup(requests.get(f'https://www.acmicpc.net/user/{bojid}').text, 'html.parser')
    text = soup.select_one('div.panel-body')
    solved = text.text.split('\n')[1:-1]
    return solved


def random_bj(author, cmd):
    args = cmd.split()
    if len(args) != 2:
        return "[!] Usage : !random_bj <tier>"
    tier = args[1]

    # 요청자 BOJ id 및 푼 문제 목록 확인
    try:
        bojid = algoalgo_sql.sql_exe("SELECT baekjoon_id FROM member WHERE discord_id = %s", author)[0]['baekjoon_id']
    except Exception as ex:
        return f"[!] An error occurs while check db....\n[INFO] error : {ex}"
    solved = get_solved(bojid)

    # 티어별 시작점 설정
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
        return "[!] There is no such tier in solved.ac."

    # DB에서 해당 티어 문제 목록 가져오기
    sql = "SELECT id FROM solved_rank WHERE rank >= %s and rank < %s;"
    try:
        result = algoalgo_sql.sql_exe(sql, startfrom, startfrom+5)
    except Exception as ex:
        return f"[!] An error occurs while check db....\n[INFO] error : {ex}"
    candidate = []
    for item in result:
        candidate.append(item['id'])

    # 푼 적 없는 랜덤 문제 추천
    count = 0
    while count != len(candidate):
        rbj = candidate[randint(0, len(candidate))]
        if rbj not in solved:
            break;

    # 결과 반환
    if count == len(candidate):
        return "[!] You've Solved All Problems."
    else:
        return f'https://www.acmicpc.net/problem/{rbj}'


def daily_baekjoon(author, cmd):
    args = cmd.split()
    if len(args) != 2:
        return "[!] Usage : !daily_baekjoon <Problem id>"

    # 입력된 문제 번호
    pid = args[1]

    # 인증된 푼 문제 목록
    try:
        solvedlist = algoalgo_sql.sql_exe("SELECT bj_solved FROM member WHERE discord_id = %s", author)[0]['bj_solved']
    except Exception as ex:
        return f"[!] An error occurs while check db....\n[INFO] error : {ex}"

    # 이미 인증된 문제
    if solvedlist == None:
        solvedlist = ""
    if pid in solvedlist.split(';')[:-1]:
        return "[!] Already Registered Problem"

    # 아직 풀지 않은 문제
    try:
        solvedlist_db = get_solved(algoalgo_sql.sql_exe("SELECT baekjoon_id FROM member WHERE discord_id = %s", author)[0]['baekjoon_id'])
    except Exception as ex:
        return f"[!] An error occurs while check db....\n[INFO] error : {ex}"
    if pid not in solvedlist_db:
        return "[!] You Haven't Solved the Problem Yet."

    # 신규 1일 1백준 인증 및 add point
    solvedlist += (str(pid) + ';')
    try:
        algoalgo_sql.sql_update("UPDATE member SET bj_solved = %s WHERE discord_id = %s", solvedlist, author)
        addpoint(f"!addpoint 11 {author}")
        algoalgo_sql.sql_update("UPDATE member SET bj_today = 1 WHERE discord_id = %s", author)
    except Exception as ex:
        return f"[!] An error occurs while update certification into db....\n[INFO] error : {ex}"

    return "[+] Successfully Certified."

def unlock(author):
    try:
        memberinfo = algoalgo_sql.sql_exe("SELECT status, map_location, baekjoon_id, bj_solved FROM member WHERE discord_id = %s", author)[0]
    except Exception as ex:
        return f"[!] An error occurs while check db....\n[INFO] error : {ex}"

    # 이미 잠금 해제된 경우
    if memberinfo['status'] == 1:
        return "[!] Already Unlocked."

    # 스턴에 걸린 경우
    if memberinfo['status'] == -1:
        return "[!] You've got Stunned. Try Again Tomorrow."

    if memberinfo['status'] == 0:
        # 풀어야 하는 문제 확인
        try:
            pid = algoalgo_sql.sql_exe("SELECT baekjoon_no FROM map WHERE id = %s", memberinfo['map_location'])[0]['baekjoon_no']
        except Exception as ex:
            return f"[!] An error occurs while check db....\n[INFO] error : {ex}"

        # 정상 해제 시도
        if pid in get_solved(memberinfo['baekjoon_id']):
            try:
                algoalgo_sql.sql_update("UPDATE member SET status = 1 WHERE baekjoon_id = %s", memberinfo['baekjoon_id'])
            except Exception as ex:
                return f"[!] An error occurs while update status into db....\n[INFO] error : {ex}"

            # DB에 인증되지 않았을 경우 인증 진행
            if pid not in memberinfo['bj_solved'].split(';')[:-1]:
                memberinfo['bj_solved'] += (str(pid) + ';')

            return "[*] Successfully Unlocked."

        # 문제를 풀지 않은 경우
        else:
            return "[!] You haven't Solved The Problem."

    # 그 외의 에러
    else:
        return "[!] Status Error: Call the Admins"

def show_items(items_list):
    try:
        item_dir = {"STEP" : 0,
        "SNAKE" : 0,
        "STUN" : 0,
        "ASSASSIN" : 0,
        "REDEMPTION" : 0,
        "CAFFEINE" : 0,
        "BOMB" : 0,
        "RED BULL" : 0
        }
        if items_list != None:    
            items_list = items_list.rstrip(';')
            items = items_list.split(';')
            for item in items:
                if len(item) == 0:
                    continue
                item_dir[item] += 1
        return item_dir
    except Exception as ex:
        raise ex
