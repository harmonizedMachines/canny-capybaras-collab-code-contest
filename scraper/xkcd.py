from typing import Optional

from scrapy.crawler import CrawlerProcess
from xkcd_spider import XKCDSpider


class XKCD():  # noqa: D101
    def __init__(self, process: Optional[CrawlerProcess]):
        self.process = process
        self.accepted_formats = ['json', 'csv']

    def __xkcd_crawl(self, start: Optional[int], finish: Optional[int],  # noqa: D102
                   save_path: Optional[str], file_format: Optional[str]) -> None:
        self.process.crawl(XKCDSpider, start, finish, save_path, file_format)
        return

    def get_certain(self,  # noqa: D102
                     start: Optional[int] = None, 
                     file_format: Optional[str] = None,
                     save_path: Optional[str] = None
                     ) -> None:  # file_format currently taking json and csv. Default is json
        if start is None:
            return

        finish = start + 1
        file_format = self.accepted_formats[0] if file_format not in self.accepted_formats else file_format
        self.__xkcd_crawl(start, finish, save_path, file_format)

    def get_range(self,  # noqa: D102
                   start: Optional[int] = None, finish: Optional[int] = None,
                   file_format: Optional[str] = None,
                   save_path: Optional[str] = None) -> None:
        if start is None or finish is None:
            return

        file_format = self.accepted_formats[0] if file_format not in self.accepted_formats else file_format
        self.__xkcd_crawl(start, finish+1, None, file_format) # inclusive 


if __name__ == '__main__':
    process = CrawlerProcess()

    xkcd = XKCD(process)
    xkcd.get_range(543, 547, 'json', "")
    process.start()
