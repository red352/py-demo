import json
import re

import scrapy

'''
最后更新时间 2023/8/15 14:50 (total 852577)
'''


def write_csv():
    with open(r'C:\Users\lenovo\Documents\my-dev\dev-project\python\demo\responsedata\gameData.txt',
              mode='a',
              encoding='utf-8') as f:
        while True:
            data = yield
            try:
                f.write(data + '\n')
            except Exception as e:
                print(e)
                pass


wc = write_csv()
next(wc)


class RawgSpider(scrapy.Spider):
    name = "rawg"
    allowed_domains = ["rawg.io"]
    start_urls = ["https://rawg.io"]

    def parse(self, response, **kwargs):
        if response.status == 200:
            data = response.text
            wc.send(str(json.loads(data)))

    def start_requests(self):
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
        base_url = 'https://api.rawg.io/api/games?key=3b101a9b738740328e939f027359a02d&page={}&page_size=40'
        for i in unreached_set:
            head_url = base_url.format(i)
            yield scrapy.Request(url=head_url)
