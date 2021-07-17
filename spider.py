import scrapy
import os
import datetime
import json
import csv

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
        self.comics.append([comic[0],comic[1]])
        self.titles.append([comic[0],comic[1].title])
        self.image_urls.append([comic[0],comic[1].image_url])


class Comic(object):
    """
    Custom object that store the title, scripts and the image_url of a comic
    """
    def __init__(self, title,script,image_url):
        self.title = title
        self.script = script
        self.image_url = image_url


class SucideSpider(scrapy.Spider):
    name = "sucide"

    def start_requests(self):
            yield scrapy.Request(url='https://xkcd.com/', callback=self.parse)

    def parse(self, response):
            return {'lastest_comic':response.xpath('/html/head/meta[4]/@content').re_first(r'\d+')}


class XKCDSpider(scrapy.Spider):
    name = "xkcd_spider"
    def __init__(self,user_input = 1 ,save_path = "",file_format = 'json',*args,**kwargs):
        super(XKCDSpider, self).__init__(*args,**kwargs)
        self.comics_objs = []
        self.user_input = user_input
        self.save_path = save_path
        self.file_format = file_format

    def start_requests(self):
        os.chdir(self.save_path)
        time = datetime.now().strftime("%d_%m_%Y_%H-%M-%S")
        os.mkdir(time)
        os.chdir(time)
        for index_i, i in enumerate(self.user_input):
            yield scrapy.Request(url='https://xkcd.com/' + str(i), callback=self.parse, cb_kwargs=dict(index=index_i))
        return {'comics_objs':self.comics_objs}

    def parse(self, response, index):
        page = response.url.split("/")[-2]

        # extract url
        comic_url = response.url
        # extract title
        title = response.xpath('//div[@id="ctitle"]/text()').extract_first()
        try:
            # extract texts
            script = response.xpath('//div[@id="comic"]//img/@title').extract_first()
            # extract comic
            image_url = "http://" + response.xpath('//div[@id="comic"]//img/@src').extract_first()[2:]
        except:
            image_url, script = "https://uniim1.shutterfly.com/render/00-vOZRc1W66JnxNvciJy8U4krEZhJw8T6sbQ90aYWJRTIu1xZykVtCbeNYqPr02Q1KldMTLfbtJ__wYVBQ_4iTow?cn=THISLIFE&res=small", ""
            print("Found a build-yourself comic, empty script and image_url")
        # export to file
        self.comics_objs.append([index, Comic(title, script, image_url)])

        filename = 'xkcd-' + page + '.png'
        item_dir = 'xkcd-' + page
        os.mkdir(item_dir)
        os.chdir(item_dir)
        if self.file_format == 'json':
            results = {'title': title, 'script': script, 'image_url': image_url, 'comic_url': comic_url}
            with open('xkcd-' + page + '.json', 'w') as f:
                json.dump(results, f)
        elif self.file_format == 'csv':
            with open('xkcd-' + page + '.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['title', 'script', 'image_url', 'comic_url'])
                writer.writerow([title, script, image_url, comic_url])
        else:
            raise KeyError(self.file_format + "isn't a supported format")
        os.chdir("..\\")
        return scrapy.Request(url=image_url, callback=self.parse_img,
                              cb_kwargs=dict(filename=filename, item_dir=item_dir))

    def parse_img(self, response, filename, item_dir):
        os.chdir(item_dir)
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
        os.chdir("..\\")

