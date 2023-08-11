import random
import string
import unittest

import redis

import csv

redis_host = '54.254.154.185'
redis_port = 6379


class MyTestCase(unittest.TestCase):

    def test_gen(self):
        def my_gen():
            for i in range(0, 10):
                yield i

        for i in my_gen():
            print(i)

    def test_csv(self):

        with open('./csv/test.csv', 'a+', newline='\n', encoding='utf-8') as f:
            csv_write = csv.writer(f)

            def my_gen(size=0):
                print(size)
                ran = random.Random()
                num = 10

                def gen_data():
                    for a in range(0, 10):
                        pass
                    yield ''.join(ran.choices(string.ascii_letters, k=4)), ran.randint(15, 60)

                # while True:
                #     print(next(gen_data()))

                def inner(inner_size=0):
                    for i in range(0, -(-inner_size // num)):
                        res = []
                        for j in range(0, num):
                            try:
                                data = next(gen_data())
                            except StopIteration:
                                print("Stop sign")
                                break
                            res.append(data)
                        else:
                            yield res
                            continue
                        break

                for i in inner(inner_size=size):
                    csv_write.writerows(i)

            my_gen(1)

    def test_redis(self):
        r_pool = redis.ConnectionPool(host=redis_host, port=redis_port, username='lyx', password='lyxsix4007')
        with redis.Redis(connection_pool=r_pool) as r:
            r.set("lyx", "123")
            print(r.get('lyx'))


if __name__ == '__main__':
    unittest.main()
