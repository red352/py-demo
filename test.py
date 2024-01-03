import ast
import json
import random
import re
import string
import threading
import time
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
                    for batch_num in range(0, -(-inner_size // num)):
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

    def test_one(self):
        with open(r'C:\Users\lenovo\Documents\my-dev\dev-project\python\demo\responsedata\tmp.json',
                  encoding='utf-8') as f:
            json_string = f.read()
            pattern = r'key=6bfe5d0d89ea48c2b22e5cec2c4d9912&page=(\d+)'
            match = re.findall(pattern, json_string)
            print(match)
            json_data = json.loads(json_string)
            print(json_data['next'])

    def test_two(self):
        unreached_set = set()
        with open(r'C:\Users\lenovo\Documents\my-dev\dev-project\python\demo\responsedata\gameData.txt',
                  encoding='utf-8') as f:
            searched_set = set()
            next_pattern = re.compile(r"'next': None")
            pattern = re.compile(r"page=(\d+)")
            for e in f:
                continue_match = next_pattern.search(e)
                if continue_match is not None:
                    new_match = pattern.search(e)
                    searched_set.add((int(new_match.group(1)) + 1))
                else:
                    match = pattern.search(e)
                if match is not None:
                    searched_page = int(match.group(1)) - 1
                    searched_set.add(searched_page)
            for i in range(1, 21316):
                if i not in searched_set:
                    unreached_set.add(i)
            print(unreached_set)

    # add esrb.csv
    def test_ersb(self):
        with open(r'C:\Users\lenovo\Documents\my-dev\dev-project\python\demo\responsedata\gameData.txt',
                  encoding='utf-8') as f:
            esrb_slug_map = dict()
            esrb_name_map = dict()
            for e in f:
                data: dict = ast.literal_eval(e)
                results: list = data.get('results')
                for result in results:
                    result: dict
                    esrb = result.get('esrb_rating')
                    esrb_id = esrb.get('id') if esrb else None
                    if esrb_id is not None:
                        esrb_name = esrb.get('name')
                        esrb_slug = esrb.get('slug')
                        esrb_name_map[esrb_id] = esrb_name
                        esrb_slug_map[esrb_id] = esrb_slug
                    if len(esrb_name_map) == 6 & len(esrb_slug_map) == 6:
                        break
                else:
                    continue
                csv_list = [(i, esrb_slug_map.get(i), esrb_name_map.get(i)) for i in range(1, 7)]
                print(csv_list)
                break
        with open(r'C:\Users\lenovo\Documents\my-dev\dev-project\python\demo\csv\esrb.csv',
                  mode='a',
                  newline='',
                  encoding='utf-8') as csv_f:
            cw = csv.writer(csv_f)
            cw.writerows(csv_list)

    def test_platform(self):
        with open(r'C:\Users\lenovo\Documents\my-dev\dev-project\python\demo\responsedata\platforms.txt',
                  encoding='utf-8') as f:
            csv_data = []
            for e in f:
                data = ast.literal_eval(e)
                results: list = data.get('results')
                for result in results:
                    result: dict
                    platform_id = result.get('id')
                    platform_name = result.get('name')
                    platform_slug = result.get('slug')
                    platform_image = result.get('image')
                    platform_year_start = result.get('year_start')
                    platform_year_end = result.get('year_end')
                    platform_games_count = result.get('games_count')
                    platform_image_background = result.get('image_background')
                    csv_data.append((platform_id, platform_name, platform_slug, platform_image, platform_year_start,
                                     platform_year_end, platform_games_count, platform_image_background))
            with open(r'C:\Users\lenovo\Documents\my-dev\dev-project\python\demo\csv\platforms.csv',
                      mode='w',
                      newline='',
                      encoding='utf-8') as csv_f:
                cw = csv.writer(csv_f)
                cw.writerows(csv_data)

    def test_parent_platform(self):
        with open(r'C:\Users\lenovo\Documents\my-dev\dev-project\python\demo\responsedata\parentPlatforms.txt',
                  encoding='utf-8') as f:
            csv_data = []
            for e in f:
                data = ast.literal_eval(e)
                results: list = data.get('results')
                for result in results:
                    result: dict
                    p_id = result.get('id')
                    p_name = result.get('name')
                    p_slug = result.get('slug')
                    csv_data.append((p_id, p_name, p_slug))
            with open(r'C:\Users\lenovo\Documents\my-dev\dev-project\python\demo\csv\parentPlatforms.csv',
                      mode='w',
                      newline='',
                      encoding='utf-8') as csv_f:
                cw = csv.writer(csv_f)
                cw.writerows(csv_data)

    def test_parent_platform_connect(self):
        with open(r'C:\Users\lenovo\Documents\my-dev\dev-project\python\demo\responsedata\parentPlatforms.txt',
                  encoding='utf-8') as f:
            csv_data = []
            for e in f:
                data = ast.literal_eval(e)
                results: list = data.get('results')
                for result in results:
                    result: dict
                    p_id = result.get('id')
                    ids = [i.get('id') for i in result.get('platforms')]
                    csv_data.append((p_id, *ids))
            with open(r'C:\Users\lenovo\Documents\my-dev\dev-project\python\demo\csv\parentPlatformsConnect.csv',
                      mode='w',
                      newline='',
                      encoding='utf-8') as csv_f:
                cw = csv.writer(csv_f)
                cw.writerows(csv_data)

    def test_store(self):
        with open(r'C:\Users\lenovo\Documents\my-dev\dev-project\python\demo\responsedata\stores.txt',
                  encoding='utf-8') as f:
            csv_data = []
            for e in f:
                data = ast.literal_eval(e)
                results: list = data.get('results')
                for result in results:
                    s_id = result.get('id')
                    s_name = result.get('name')
                    s_domain = result.get('domain')
                    s_slug = result.get('slug')
                    s_games_count = result.get('games_count')
                    s_image_background = result.get('image_background')
                    csv_data.append((s_id, s_name, s_domain, s_slug, s_games_count, s_image_background))
            with open(r'C:\Users\lenovo\Documents\my-dev\dev-project\python\demo\csv\stores.csv',
                      mode='w',
                      newline='',
                      encoding='utf-8') as csv_f:
                cw = csv.writer(csv_f)
                cw.writerows(csv_data)

    def test_tags(self):
        with open(r'C:\Users\lenovo\Documents\my-dev\dev-project\python\demo\responsedata\tags.txt',
                  encoding='utf-8') as f:
            csv_data = []
            id_map = {}
            for e in f:
                data = ast.literal_eval(e)
                results: list = data.get('results')
                for result in results:
                    t_id = result.get('id')
                    # 去重操作
                    if id_map.get(t_id) == 1:
                        continue
                    else:
                        id_map[t_id] = 1
                    t_name = result.get('name')
                    t_slug = result.get('slug')
                    t_games_count = result.get('games_count')
                    t_image_background = result.get('image_background')
                    t_language = result.get('language')
                    csv_data.append((t_id, t_name, t_slug, t_games_count, t_image_background, t_language))
            with open(r'C:\Users\lenovo\Documents\my-dev\dev-project\python\demo\csv\tags.csv',
                      mode='w',
                      newline='',
                      encoding='utf-8') as csv_f:
                cw = csv.writer(csv_f)
                cw.writerows(csv_data)

    def test_genre(self):
        with open(r'C:\Users\lenovo\Documents\my-dev\dev-project\python\demo\responsedata\genres.txt',
                  encoding='utf-8') as f:
            csv_data = []
            for e in f:
                data = ast.literal_eval(e)
                results: list = data.get('results')
                for result in results:
                    g_id = result.get('id')
                    g_name = result.get('name')
                    g_slug = result.get('slug')
                    g_games_count = result.get('games_count')
                    g_image_background = result.get('image_background')
                    csv_data.append((g_id, g_name, g_slug, g_games_count, g_image_background))
        with open(r'C:\Users\lenovo\Documents\my-dev\dev-project\python\demo\csv\genres.csv',
                  mode='w',
                  newline='',
                  encoding='utf-8') as csv_f:
            cw = csv.writer(csv_f)
            cw.writerows(csv_data)

    def test_game(self):
        gg_map = {}
        lock = threading.Lock()
        csv_game_data = []
        csv_g_platform_data = []
        csv_g_genre_data = []
        csv_g_store_data = []
        csv_g_tag_data = []
        csv_g_screenshot_data = []
        loop_size = 1000
        loop_tmp = 0

        def write_data():
            with open(r'C:\Users\lenovo\Documents\my-dev\dev-project\python\demo\csv\game.csv',
                      mode='w',
                      newline='',
                      encoding='utf-8') as c_game:
                game_writer = csv.writer(c_game)
                with open(r'C:\Users\lenovo\Documents\my-dev\dev-project\python\demo\csv\gamePlatform.csv',
                          mode='w',
                          newline='',
                          encoding='utf-8') as c_game_platform:
                    game_platform_writer = csv.writer(c_game_platform)
                    with open(r'C:\Users\lenovo\Documents\my-dev\dev-project\python\demo\csv\gameGenre.csv',
                              mode='w',
                              newline='',
                              encoding='utf-8') as c_game_genre:
                        game_genre_writer = csv.writer(c_game_genre)
                        with open(r'C:\Users\lenovo\Documents\my-dev\dev-project\python\demo\csv\gameStore.csv',
                                  mode='w',
                                  newline='',
                                  encoding='utf-8') as c_game_store:
                            game_store_writer = csv.writer(c_game_store)
                            with open(r'C:\Users\lenovo\Documents\my-dev\dev-project\python\demo\csv\gameTag.csv',
                                      mode='w',
                                      newline='',
                                      encoding='utf-8') as c_game_tag:
                                game_tag_writer = csv.writer(c_game_tag)
                                with open(
                                        r'C:\Users\lenovo\Documents\my-dev\dev-project\python\demo\csv'
                                        r'\gameScreenshot.csv',
                                        mode='w',
                                        newline='',
                                        encoding='utf-8') as c_game_screenshot:
                                    game_screenshot_writer = csv.writer(c_game_screenshot)
                                    while True:
                                        yield
                                        with lock:
                                            game_writer.writerows(csv_game_data)
                                            game_platform_writer.writerows(csv_g_platform_data)
                                            game_genre_writer.writerows(csv_g_genre_data)
                                            game_store_writer.writerows(csv_g_store_data)
                                            game_tag_writer.writerows(csv_g_tag_data)
                                            game_screenshot_writer.writerows(csv_g_screenshot_data)
                                            csv_game_data.clear()
                                            csv_g_platform_data.clear()
                                            csv_g_genre_data.clear()
                                            csv_g_store_data.clear()
                                            csv_g_tag_data.clear()
                                            csv_g_screenshot_data.clear()

        with open(r'C:\Users\lenovo\Documents\my-dev\dev-project\python\demo\responsedata\gameData.txt',
                  encoding='utf-8') as f:

            csv_writer = write_data()
            next(csv_writer)

            for e in f:
                if loop_tmp == loop_size:
                    # TODO 写入csv
                    csv_writer.send(None)
                    print(loop_tmp)
                    loop_tmp = 0
                loop_tmp += 1
                # 使用eval更快，这里忽略字符串的安全性
                data: dict = eval(e)
                results: list = data.get('results')
                for result in results:
                    result: dict
                    g_id = result.get('id')
                    if gg_map.get(g_id) == 1:
                        continue
                    gg_map[g_id] = 1
                    g_slug = result.get('slug')
                    g_name = result.get('name')
                    g_released = result.get('released')
                    g_tba = str(result.get('tba')).lower()
                    g_background_image = result.get('background_image')
                    g_rating = result.get('rating')
                    g_rating_top = result.get('rating_top')
                    g_metacritic = result.get('metacritic')
                    g_playtime = result.get('playtime')
                    g_esrb_id = result.get('esrb_rating').get('id') if result.get('esrb_rating') else None
                    csv_game_data.append((g_id, g_slug, g_name, g_released, g_tba, g_background_image
                                          , g_rating, g_rating_top, g_metacritic, g_playtime, g_esrb_id))
                    # 游戏和平台关联
                    g_platforms: list = result.get('platforms')
                    for g_platform in g_platforms:
                        g_platform: dict
                        g_p_id = g_platform.get('platform').get('id')
                        g_p_released_at = g_platform.get('released_at')
                        g_p_requirements = g_platform.get('requirements_en')
                        csv_g_platform_data.append((g_id, g_p_id, g_p_released_at, g_p_requirements))

                    # 游戏和流派关联
                    g_genres: list = result.get('genres')
                    for g_genre in g_genres:
                        g_g_id = g_genre.get('id')
                        csv_g_genre_data.append((g_id, g_g_id))

                    # 游戏和商店关联
                    g_stores: list = result.get('stores')
                    for g_store in g_stores:
                        g_s_id = g_store.get('store').get('id')
                        csv_g_store_data.append((g_id, g_s_id))

                    # 游戏和标签关联
                    g_tags: list = result.get('tags')
                    for g_tag in g_tags:
                        g_t_id = g_tag.get('id')
                        csv_g_tag_data.append((g_id, g_t_id))

                    # 游戏和截图关联
                    g_ss_s: list = result.get('short_screenshots')
                    for g_ss in g_ss_s:
                        g_ss_id = g_ss.get('id')
                        g_ss_image = g_ss.get('image')
                        csv_g_screenshot_data.append((g_id, g_ss_id, g_ss_image))
            csv_writer.send(None)
            # just wait for io done
            time.sleep(6)

    def test_tmp(self):
        with open(r'C:\Users\lenovo\Documents\my-dev\dev-project\python\demo\csv\game.csv',
                  encoding='utf-8') as c:
            cr = csv.reader(c)
            name = []
            for e in cr:
                name.append(e[1])
            name.sort(key=lambda x: len(x),reverse=True)
            print(name[0])
            print(len(name[0]))


if __name__ == '__main__':
    unittest.main()
