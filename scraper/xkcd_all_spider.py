import csv
import json
import os
import logging
from typing import Generator, Optional

import scrapy


class XKCDAllSpider(scrapy.Spider):  # noqa: D101
    name = "xkcd_all"

    def __init__(self,
                 save_path: Optional[str] = None, file_format: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = ['https://xkcd.com/1/']
        self.start = 1
        self.save_path = save_path
        self.save_path_original = save_path
        self.file_format = file_format

    def parse(self,  # noqa: D102
              response: Optional[scrapy.http.response.html.HtmlResponse]) -> None:
        page = response.url.split("/")[-2]

        # extract title
        try:
            title = response.xpath('//div[@id="ctitle"]/text()').extract_first()
        except Exception:
            self.log(f"Could not scrape comic title", level=logging.ERROR)
            title=None
            pass

        # extract text
        try:
            text = response.xpath('//div[@id="comic"]//img/@title').extract_first()
        except Exception:
            self.log(f"Could not scrape comic text", level=logging.ERROR)
            text = None
            pass


        # extract comic
        filename = 'xkcd-' + page + '.png'
        try:
            image_url = "http://" + response.xpath('//div[@id="comic"]//img/@src').extract_first()[2:]
        except Exception:
            self.log(f"Could not scrape comic image", level=logging.ERROR)
            image_url = None
            pass

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
            results = {'title': title, 'text': text, 'image_url': image_url, 'comic_url': response.url}

            try:
                with open(self.save_path + '/xkcd-' + page + '.json', 'w') as f:
                    json.dump(results, f)
            except FileNotFoundError:
                raise "Save path does not exist, or cannot find save path"
            finally:
                self.log(f'Saved file xkcd-{page}.json')

        elif self.file_format == 'csv':
            headers = ['title', 'text', 'image source']
            data = {'title': title, 'text': text, 'image_url': image_url, 'comic_url': response.url}

            try:
                with open('xkcd-' + page + '.csv', 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=headers)
                    writer.writeheader()
                    writer.writerow(data)
            except FileNotFoundError:
                raise "Save path does not exist, or cannot find save path"
            finally:
                self.log(f'Saved file xkcd-{page}.csv')

        if image_url is not None:
            yield scrapy.Request(url=image_url, callback=self.parse_img, cb_kwargs=dict(filename=filename, save_path=self.save_path))

        next_page = response.xpath('//a[@rel="next"]/@href').extract_first()

        if next_page:
            try:
                yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
            except Exception:
                pass

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
