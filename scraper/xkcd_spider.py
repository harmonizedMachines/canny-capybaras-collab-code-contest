import csv
import json
import os
from typing import Generator, Optional

import scrapy


class XKCDSpider(scrapy.Spider):  # noqa: D101
    name = "quotes"

    def __init__(self,
                 start: Optional[int] = None, finish: Optional[int] = None,
                 save_path: Optional[str] = None, file_format: Optional[str] = None, **kwargs):

        super().__init__(**kwargs)
        self.start_url = 'https://xkcd.com/'
        self.start = start
        self.finish = finish
        self.save_path = save_path
        self.save_path_original = save_path
        self.file_format = file_format

    def start_requests(self) -> Generator[scrapy.http.request.Request, None, None]:  # noqa: D102
        for i in range(self.start, self.finish):
            yield scrapy.Request(url=self.start_url + str(i), callback=self.parse)

    def parse(self,  # noqa: D102
              response: Optional[scrapy.http.response.html.HtmlResponse]) -> scrapy.http.request.Request:
              
        page = response.url.split("/")[-2]

        # extract title
        title = response.xpath('//div[@id="ctitle"]/text()').extract()[0]

        # extract text
        text = response.xpath('//div[@id="comic"]//img/@title').extract()[0]

        # extract comic
        filename = 'xkcd-' + page + '.png'
        image_url = "http://" + response.xpath('//div[@id="comic"]//img/@src').extract()[0][2:]

        # making folder for files
        try:
            parent_dir = "../output" if self.save_path_original is None else self.save_path_original
            directory = "xkcd-" + page
            self.save_path = os.path.join(parent_dir, directory)
            os.mkdir(self.save_path)
        except FileExistsError:
            pass

        # export to file
        if self.file_format == 'json':
            results = {'title': title, 'text': text, 'image source': image_url}

            try:
                with open(self.save_path + '/xkcd-' + page + '.json', 'w') as f:
                    json.dump(results, f)
            except FileNotFoundError:
                raise "Save path does not exist, or cannot find save path"

        elif self.file_format == 'csv':
            headers = ['title', 'text', 'image source']
            data = {'title': title, 'text': text, 'image source': image_url}

            try:
                with open('xkcd-' + page + '.csv', 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=headers)
                    writer.writeheader()
                    writer.writerow(data)
            except FileNotFoundError:
                raise "Save path does not exist, or cannot find save path"

        return scrapy.Request(url=image_url, callback=self.parse_img, cb_kwargs=dict(filename=filename, save_path=self.save_path))

    # Creating image for comic
    def parse_img(self,  # noqa: D102
                  response: Optional[scrapy.http.response.Response],
                  filename: Optional[str],
                  save_path: Optional[str]) -> None:

        try:
            with open(save_path + "/" + filename, 'wb') as f:
                f.write(response.body)
        except FileNotFoundError:
            raise "Save path does not exist, or cannot find save path"
        finally:
            self.log(f'Saved file {filename}')
