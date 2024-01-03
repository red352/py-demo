import json

import scrapy

'''
最后更新时间 2023/8/16 10:24 (total 10)
'''


class StoresSpider(scrapy.Spider):
    name = "stores"
    allowed_domains = ["rawg.io"]
    start_urls = ["https://api.rawg.io/api/stores?key=3b101a9b738740328e939f027359a02d&page=1&page_size=40"]

    def parse(self, response, **kwargs):
        res = response.text
        res_json = json.loads(res)
        # wc.send(str(res_json))
        with open(r'C:\Users\lenovo\Documents\my-dev\dev-project\python\demo\responsedata\stores.txt',
                  mode='a',
                  encoding='utf-8') as f:
            try:
                f.write(str(res_json) + '\n')
            except Exception as e:
                print(e)
                pass
        next_url = res_json['next']
        if next_url is not None:
            yield scrapy.Request(url=next_url, callback=self.parse)
