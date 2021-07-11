from importlib import find_loader
import scrapy

from typing import Optional
from scrapy.crawler import CrawlerProcess

from xkcd_spider import XKCDSpider


class XKCD():
    def __init__(self, process):
        self.process = process
        self.accepted_formats = ['json', 'csv']


    def xkcd_crawl(self, start, finish, save_path, file_format):
        self.process.crawl(XKCDSpider, start, finish, save_path, file_format)
        return

    def xkcd_certain(self, start: Optional[int]=None, file_format: Optional[str]=None): # file_format currently taking json and csv. Default is json
        if start is None:
            return

        finish = start + 1
        file_format =  self.accepted_formats[0] if file_format not in self.accepted_formats else file_format
        self.xkcd_crawl(start, finish, None, file_format)

    def xkcd_range(self, start: Optional[int]=None, finish: Optional[int]=None, file_format: Optional[str]=None):
        if start is None or finish is None:
            return

        file_format =  self.accepted_formats[0] if file_format not in self.accepted_formats else file_format
        self.xkcd_crawl(start, finish, None, file_format)


if __name__ == '__main__':
    process = CrawlerProcess()

    xkcd = XKCD(process)
    xkcd.xkcd_range(60, 70, 'json')
    process.start()