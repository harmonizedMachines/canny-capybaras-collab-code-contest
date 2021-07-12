import scrapy
from scrapy.crawler import CrawlerProcess
import json
import csv
import os
from datetime import datetime


class Container(object):
    """
    Container that contains 3 lists ('comics' for the list of comics that have been crawled,
    'titles' for the list of all comic's titles that have been crawled and
    'image_urls' for the list of all comic's image's url that have been crawled)
    """
    def __init__(self):
        self.comics = []
        self.titles = []
        self.image_urls = []

    def append(self, comic):
        """
        Append lists with comic's propreties
        :param comic

        """
        self.comics.append(comic)
        self.titles.append(comic.title)
        self.image_urls.append(comic.image_url)


class Comic(object):
    """
    Custom object that store the title, scripts and the image_url of a comic
    """
    def __init__(self, title,script,image_url):
        self.title = title
        self.script = script
        self.image_url = image_url


def crawl(user_input, file_format='json', save_path="."):
    """
    mode : list, must define the :param 'list_' with a list
    mode : range, must define the :param 'start' and the :param 'end' with integers
    :param file_format , by default 'json' ,can be changed to 'csv'
    :param save_path , in working directory by default, can by change by a str path
    """
    comics_objs = Container()  # creation of a Container

    user_input = user_input.split(',')
    for input in user_input:
        if '-' in input:
            split_input = input.split('-')
            user_input = [*user_input,*range(int(split_input[0]),int(split_input[1])+1)]
            user_input.remove(input)
    user_input = [int(input) for input in user_input]

    class XKCDSpider(scrapy.Spider):
        name = "xkcd_spider"

        def __init__(self, user_input, save_path, file_format, **kwargs):
            super().__init__(**kwargs)
            self.start_url = 'https://xkcd.com/'
            self.user_input = user_input
            self.save_path = save_path
            self.file_format = file_format

        def start_requests(self):
            os.chdir(self.save_path)
            time = datetime.now().strftime("%d_%m_%Y_%H-%M-%S")
            os.mkdir(time)
            os.chdir(time)
            for i in self.user_input:
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
            item_dir = 'xkcd-' + page
            os.mkdir(item_dir)
            os.chdir(item_dir)
            if self.file_format == 'json':
                results = {'title': title, 'script': script, 'image_url': image_url}
                with open('xkcd-' + page + '.json', 'w') as f:
                    json.dump(results, f)
            elif self.file_format == 'csv':
                with open('xkcd-' + page + '.csv', 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['title', 'script', 'image_url'])
                    writer.writerow([title, script, image_url])
            else:
                raise KeyError(self.file_format+"isn't a supported format")
            os.chdir("..\\")
            return scrapy.Request(url=image_url, callback=self.parse_img, cb_kwargs=dict(filename=filename,item_dir=item_dir))

        def parse_img(self, response, filename,item_dir):
            os.chdir(item_dir)
            with open(filename, 'wb') as f:
                f.write(response.body)
            self.log(f'Saved file {filename}')
            os.chdir("..\\")

    process = CrawlerProcess()
    process.crawl(XKCDSpider,user_input=user_input, file_format=file_format, save_path=save_path)
    process.start()
    return comics_objs


if __name__ == "__main__":
    print(crawl(user_input='5,7,10-15',file_format="json").titles)