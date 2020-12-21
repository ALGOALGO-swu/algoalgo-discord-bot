import algoalgo_sql
import algoalgo_member
import algoalgo_error

def getBossLife():
    sql = "select life from algoalgo.boss limit 1"
    try:
        sql_result = algoalgo_sql.sql_exe(sql)
        curr_life = sql_result[0]['life']

        return curr_life
    except Exception as ex:
        raise ex


def attackBoss(author, cmd):
    args = cmd.split()
    if len(args) != 2:
        return "[!] Usage : !attackBoss <Problem id>"

    # 입력된 문제 번호
    pid = args[1]

    # 인증된 푼 문제 목록
    try:
        solvedlist = algoalgo_sql.sql_exe("SELECT bj_solved FROM member WHERE discord_id = %s", author)[0]['bj_solved']
    except Exception as ex:
        return f"[!] An error occurs while check db....\n[INFO] error : {ex}"

    if solvedlist == None:
        solvedlist = ""

    # 이미 인증된 문제
    if pid in solvedlist.split(';')[:-1]:
        return "[!] Already Registered Problem"

    # 아직 풀지 않은 문제
    try:
        solvedlist_db = algoalgo_member.get_solved(algoalgo_sql.sql_exe("SELECT baekjoon_id FROM member WHERE discord_id = %s", author)[0]['baekjoon_id'])
    except Exception as ex:
        return f"[!] An error occurs while check db....\n[INFO] error : {ex}"
    if pid not in solvedlist_db:
        return "[!] You Haven't Solved the Problem Yet."

    # 문제풀이 인증 및 add point
    solvedlist += (str(pid) + ';')
    try:
        algoalgo_sql.sql_update("UPDATE member SET bj_solved = %s WHERE discord_id = %s", solvedlist, author)
    except Exception as ex:
        return f"[!] An error occurs while update certification into db....\n[INFO] error : {ex}"

    # 문제 계수 설정 
    rank = algoalgo_sql.sql_exe("SELECT rank FROM algoalgo.solved_rank where id = %s", pid)[0]['rank']
    dmg = 0
    if rank <= 5:
        dmg = 1 
    elif rank <= 10:
        dmg = 3
    elif rank <= 15:
        dmg = 8
    else :
        dmg = 15

    dmg *= (rank-1)%5 + 1

    # 보스 체력 날리기
    try:
        algoalgo_sql.sql_update("UPDATE boss SET life = life - %s where season = 1;", dmg)
    except Exception as ex:
        return f"[!] An error occurs while updating boss life into db....\n[INFO] error : {ex}"

    # 멤버당 보스 공격한 누적 뎀 정리
    try:
        algoalgo_sql.sql_update("UPDATE member_boss SET attack = attack + 1 where discord_id = %s;", author)
        algoalgo_sql.sql_update("UPDATE member_boss SET total_dmg = total_dmg + %s where discord_id = %s;", dmg, author)
    except Exception as ex:
        return f"[!] An error occurs while updating boss life into db....\n[INFO] error : {ex}"

    return f"[+] 공격 성공, 데미지 : {dmg}"