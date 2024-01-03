import csv
import json

import scrapy


def write_csv():
    with open(r'C:\Users\lenovo\Documents\my-dev\dev-project\python\demo\responsedata\eventsOnDay.txt',
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


class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com"]

    def parse(self, response, **kwargs):
        if response.status == 200:
            data = response.text
            wc.send(str(json.loads(data)))

    def start_requests(self):
        base_url = 'https://baike.baidu.com/cms/home/eventsOnHistory/{}.json'
        for i in range(1, 13):
            tmp_str = str(i)
            str_num = tmp_str.zfill(2) if len(tmp_str) == 1 else tmp_str
            head_url = base_url.format(str_num)
            yield scrapy.Request(url=head_url)
