import scrapy
from scrapy.crawler import CrawlerProcess
import json


class Container(object):
    def __init__(self):
        self.comics = []
        self.titles = []
        self.image_urls = []

    def append(self, comic):
        self.comics.append(comic)
        self.titles.append(comic.title)
        self.image_urls.append(comic.image_url)


class Comic(object):
    def __init__(self, title,script,image_url):
        self.title = title
        self.script = script
        self.image_url = image_url


def crawl(start, finish, file_format='json', save_path=""):
    comics_objs = Container()

    class XKCDSpider(scrapy.Spider):
        name = "xkcd_spider"

        def __init__(self, start, finish, save_path, file_format, **kwargs):
            super().__init__(**kwargs)
            self.start_url = 'https://xkcd.com/'
            self.start = start
            self.finish = finish
            self.save_path = save_path
            self.file_format = file_format

        def start_requests(self):
            for i in range(self.start, self.finish+1):
                yield scrapy.Request(url=self.start_url + str(i), callback=self.parse)

        def parse(self, response):
            page = response.url.split("/")[-2]
            # extract title
            title = response.xpath('//div[@id="ctitle"]/text()').extract()[0]
            # extract text
            script = response.xpath('//div[@id="comic"]//img/@title').extract()[0][1:-1].split("' '")
            # extract comic
            filename = 'xkcd-' + page + '.png'
            image_url = "http://" + response.xpath('//div[@id="comic"]//img/@src').extract()[0][2:]
            # export to file
            comics_objs.append(Comic(title,script,image_url))
            if self.file_format == 'json':
                results = {'title': title, 'script': script, 'image_source': image_url}
                with open('xkcd-' + page + '.json', 'w') as f:
                    json.dump(results, f)
            elif self.file_format == 'csv':
                pass
            return scrapy.Request(url=image_url, callback=self.parse_img, cb_kwargs=dict(filename=filename))

        def parse_img(self, response, filename):
            with open(filename, 'wb') as f:
                f.write(response.body)
            self.log(f'Saved file {filename}')
    process = CrawlerProcess()
    process.crawl(XKCDSpider, start=start, finish=finish, file_format=file_format, save_path=save_path)
    process.start()
    return comics_objs

if __name__ == "__main__":
    print(crawl(8,9).titles)
