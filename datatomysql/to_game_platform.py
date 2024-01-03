import csv

import mysql.connector


def add_game_platform_mysql():
    with mysql.connector.connect(host="47.113.231.122", user="root", password="123456", database="rawg") as m:
        with m.cursor() as cur:
            data = []
            loop_size = 1000
            loop_tmp = 0
            sql = "insert into game_platform (g_id, platform_id, released_at, requirements) values (%s,%s,%s,%s)"

            def insert_sql():
                cur.executemany(
                    sql,
                    data)
                m.commit()

            with open(r'C:\Users\lenovo\Documents\my-dev\dev-project\python\demo\csv\gamePlatform.csv',
                      encoding='utf-8') as c:
                cr = csv.reader(c)
                for e in cr:
                    if loop_tmp == loop_size:
                        insert_sql()
                        data.clear()
                        loop_tmp = 0
                    loop_tmp += 1
                    e = [None if i == '' else i for i in e]
                    data.append(e)
                insert_sql()


if __name__ == '__main__':
    add_game_platform_mysql()
