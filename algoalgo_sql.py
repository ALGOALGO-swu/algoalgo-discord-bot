import pymysql
import os

db_conn = pymysql.connect(
    user='staff', 
    passwd=os.environ['db_pass'],
    host='34.64.120.154', 
    db='algoalgo', 
    charset='utf8'
)

def sql_update(query, *args):
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

    cursor = db_conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute(query, args)

        result = cursor.fetchall()

        db_conn.commit()
        db_conn.close()

        print(result)
        return result

    except Exception as ex:
        raise ex