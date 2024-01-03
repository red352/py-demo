import json

import scrapy

'''
最后更新时间 2023/8/16 10:33 (total 9657)
'''


class TagsSpider(scrapy.Spider):
    name = "tags"
    allowed_domains = ["rawg.io"]
    start_urls = ["https://api.rawg.io/api/tags?key=3b101a9b738740328e939f027359a02d&page=1&page_size=40"]

    def parse(self, response, **kwargs):
        res = response.text
        res_json = json.loads(res)
        # wc.send(str(res_json))
        with open(r'C:\Users\lenovo\Documents\my-dev\dev-project\python\demo\responsedata\tags.txt',
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
