import csv

import mysql.connector


def add_platform_mysql():
    with mysql.connector.connect(host="47.113.231.122", user="root", password="123456", database="rawg") as m:
        with m.cursor() as cur:
            data = []
            with open(r'C:\Users\lenovo\Documents\my-dev\dev-project\python\demo\csv\tags.csv',
                      encoding='utf-8') as c:
                cr = csv.reader(c)
                for e in cr:
                    data.append(e)
            cur.executemany(
                "insert into tags (id,name,slug,games_count,image_background,language) values (%s,%s,%s,%s,%s,%s)",
                data)
            m.commit()


if __name__ == '__main__':
    add_platform_mysql()
