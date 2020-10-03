import algoalgo_sql
import algoalgo_error
import algoalgo_item
import algoalgo_map


def check_dailystep(author):
    sql = f"select daily_steps from member where discord_id='{str(author)}'"
    try:
        sql_result=algoalgo_sql.sql_exe(sql)
        daily_step = sql_result[0]['daily_steps']
        
        return daily_step
    except Exception as ex:
        raise ex

def update_dailystep(author):
    sql = f"update member set daily_steps = daily_steps + 1 where discord_id='{str(author)}'"    
    try:
        algoalgo_sql.sql_update(sql)
        return 0
    except Exception as ex:
        raise ex

def check_status(author):
    sql = f"select status from member where discord_id='{str(author)}'"
    try:
        sql_result=algoalgo_sql.sql_exe(sql)
        status = sql_result[0]['status']
        
        return status

    except Exception as ex:
        raise ex

def update_status(author):
    sql = f"update member set status = 0 where discord_id='{str(author)}'"    
    try:
        algoalgo_sql.sql_update(sql)
        return 0
    except Exception as ex:
        raise ex


# 가변인자 처리 할 수 있으면 함수 합치기
def update_location(author):
    sql = f"update member set map_location = map_location + 1 where discord_id='{str(author)}'"    
    try:
        algoalgo_sql.sql_update(sql)
        return 0
    except Exception as ex:
        raise ex

def update_location_dst(author, dst):
    sql = f"update member set map_location = {dst} where discord_id='{str(author)}'"    
    try:
        algoalgo_sql.sql_update(sql)
        return 0
    except Exception as ex:
        raise ex

def go_back(author, dst):
    sql = f"update member set map_location = map_location - 1 where discord_id='{str(author)}'"    
    try:
        algoalgo_sql.sql_update(sql)
        return 0
    except Exception as ex:
        raise ex
    
def get_location(author):
    sql = f"select map_location from member where discord_id='{str(author)}'"
    try:
        sql_result=algoalgo_sql.sql_exe(sql)
        location = sql_result[0]['map_location']
        
        return location

    except Exception as ex:
        raise ex

def check_feature(author):
    try:
        location = get_location(author)

        sql = f"select * from map where id='{location}'"
        sql_result = algoalgo_sql.sql_exe(sql)
        feature = sql_result[0]['feature']

        return feature

    except Exception as ex:
        raise ex

def ladder(author):
    try:
        location = get_location(author)

        sql = f"select ahead_to from map where id='{location}'"
        sql_result = algoalgo_sql.sql_exe(sql)
        dst = sql_result[0]['ahead_to']

        update_location_dst(author, dst)


    except Exception as ex:
        raise ex

def snake(author):
    try:
        location = get_location(author)

        sql = f"select ahead_to from map where id='{location}'"
        sql_result = algoalgo_sql.sql_exe(sql)
        dst = sql_result[0]['ahead_to']

        update_location_dst(author, dst)


    except Exception as ex:
        raise ex

def check_items(author, item_name):
    sql = f"select items from member where discord_id='{str(author)}'"
    try:
        sql_result=algoalgo_sql.sql_exe(sql)
        item_dir = show_items(sql_result[0]['items'])
        
        return item_dir[item_name]
    except Exception as ex:
        raise ex

def use_items(author, item):
    sql = f"select items from member where discord_id='{str(author)}'"
    try:
        sql_result=algoalgo_sql.sql_exe(sql)
        item_dir = show_items(sql_result[0]['items'])
        item_dir[item] -= 1
        if item_dir[item] < 0:
            e_msg = "You tried to use item you don't have.\n보유하지 않은 아이템을 사용하려 하셨습니다. 스탭에게 문의주세요."
            raise algoalgo_error.UserDefinedException(e_msg)

        item_str = ""
        for k, v in item_dir.items():
            if v <= 0:
                continue
            item_str += (k+';')*v

        update_query = f"update member set items = %s where discord_id=%s;"
        algoalgo_sql.sql_update(update_query, item_str, str(author))
        
    except Exception as ex:
        raise ex

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

