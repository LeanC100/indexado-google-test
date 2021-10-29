import pymysql

def connectDatabase():
    con = pymysql.connect(host='10.1.193.4',
    user='metabase',
    password='metabase',
    db='data_seo',
    port=30336,
    charset='utf8mb4')

    cursor=con.cursor()

    return cursor,con


def executeQuery(cursor,con, data):
    try:
        cursor.execute(data)
        con.commit()
        cursor.close()
        con.close()
        return True
    except Exception as e:
        print(e)
        return False
