import scrapy
import json
import csv
from typing import Optional


class XKCDSpider(scrapy.Spider):
    name = "quotes"

    def __init__(self, start: Optional[int]=None, finish: Optional[int]=None, save_path: Optional[str]=None, file_format: Optional[str]=None, **kwargs):
        super().__init__(**kwargs)
        self.start_url = 'https://xkcd.com/'
        self.start = start
        self.finish = finish
        self.save_path = save_path
        self.file_format = file_format

    def start_requests(self):
        for i in range(self.start, self.finish):
            yield scrapy.Request(url=self.start_url + str(i), callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        # extract title
        title = response.xpath('//div[@id="ctitle"]/text()').extract()[0]
        # extract text
        text = response.xpath('//div[@id="comic"]//img/@title').extract()[0]
        # extract comic
        filename = 'xkcd-' + page + '.png'
        image_url = "http://" + response.xpath('//div[@id="comic"]//img/@src').extract()[0][2:]

        # export to file
        if self.file_format == 'json':
            results = {'title': title, 'text': text, 'image source': image_url}
            
            with open('xkcd-' + page + '.json', 'w') as f:
                json.dump(results, f)

        elif self.file_format == 'csv':
            headers = ['title', 'text', 'image source']
            data = {'title': title, 'text': text, 'image source': image_url}

            with open('xkcd-' + page + '.csv', 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerow(data)

        return scrapy.Request(url=image_url, callback=self.parse_img, cb_kwargs=dict(filename=filename))

    def parse_img(self, response, filename):
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')