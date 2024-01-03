import csv

import mysql.connector


def add_parent_platform_connect_mysql():
    with mysql.connector.connect(host="47.113.231.122", user="root", password="123456", database="rawg") as m:
        with m.cursor() as cur:
            with open(r'C:\Users\lenovo\Documents\my-dev\dev-project\python\demo\csv\parentPlatformsConnect.csv',
                      encoding='utf-8') as c:
                cr = csv.reader(c)
                f_sql = 'update platform set p_id = %s where id in ({})'
                for e in cr:
                    sql = f_sql.format(','.join(['%s'] * (len(e) - 1)))
                    print(sql)
                    cur.execute(sql, e)
            m.commit()


if __name__ == '__main__':
    add_parent_platform_connect_mysql()
