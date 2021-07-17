# Temporary:
# flake8: noqa

import csv
import json
import operator
import os
from datetime import datetime
import _thread
import curses

import scrapy
from scrapy.crawler import CrawlerProcess


def running_loop(screen, button, app):
    global stop
    stop = False
    while 1:
        assert not stop
        ch = screen.getch()
        if ch == curses.KEY_RESIZE:
            curses.curs_set(0)
            app.draw_menu(screen)
        elif ch == curses.KEY_MOUSE:
            _, mouse_x, mouse_y, _, mouse_state = curses.getmouse()
            if not mouse_state:
                 click = button.try_click(mouse_y, mouse_x)
                 app.draw_menu(screen)
                 stop = True
                 
    

class Container(object):
    """
    Container that contains 3 lists ('comics' for the list of comics that have been crawled,
    'titles' for the list of all comic's titles that have been crawled and
    'image_urls' for the list of all comic's image's url that have been crawled)
    """
    def __init__(self):
        self.comics = []
        self.pages = []
        self.titles = []
        self.scripts = []
        self.image_urls = []
        self.comic_urls = []
        self.image_paths = []
        self.lastest_comic = ""

    def append(self, comic):
        """
        Append lists with comic's propreties
        :param comic

        """
        self.comics.append([comic[0],comic[1]])
        self.pages.append([comic[0],comic[1].page])
        self.titles.append([comic[0],comic[1].title])
        self.scripts.append([comic[0],comic[1].script])
        self.image_urls.append([comic[0],comic[1].image_url])
        self.comic_urls.append([comic[0],comic[1].comic_url])
        self.image_paths.append([comic[0],comic[1].image_path])

    def lc(self,lastest_comic):
        self.lastest_comic = lastest_comic


class Comic(object):
    """
    Custom object that store the title, scripts and the image_url of a comic
    """
    def __init__(self, page,title,script,image_url,comic_url,image_path):
        self.page = page
        self.title = title
        self.script = script
        self.image_url = image_url
        self.comic_url = comic_urlprint
        self.image_path = image_path


def crawl(user_input, screen, app, button, file_format='json', save_path="."):
    """
    mode : list, must define the :param 'list_' with a list
    mode : range, must define the :param 'start' and the :param 'end' with integers
    :param file_format , by default 'json' ,can be changed to 'csv'
    :param save_path , in working directory by default, can by change by a str path
    """
    comics_objs = Container()  # creation of a Container

    _thread.start_new_thread(running_loop,(screen, button, app))

    user_input = user_input.split(',')
    for index_input,input_ in enumerate(user_input):
        if '-' in input_:
            split_input = input_.split('-')
            str_range = [str(int_)for int_ in range(int(split_input[0]),int(split_input[1])+1)]
            user_input[index_input:index_input] = str_range
            user_input.remove(input_)
    user_input = [int(input_) for input_ in user_input]

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
            self.time = datetime.now().strftime("%d_%m_%Y_%H-%M-%S")
            os.mkdir(self.time)
            yield scrapy.Request(url=self.start_url, callback=self.parse_lc)
            for index_i, i in enumerate(self.user_input):
                yield scrapy.Request(url=self.start_url+str(i), callback=self.parse, cb_kwargs=dict(index=index_i))
                assert not stop

        def parse_lc(self,response):
            comics_objs.lc(response.xpath('/html/head/meta[4]/@content').re_first(r'\d+'))

        def parse(self, response,index):
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
                image_url,script = "https://uniim1.shutterfly.com/render/00-vOZRc1W66JnxNvciJy8U4krEZhJw8T6sbQ90aYWJRTIu1xZykVtCbeNYqPr02Q1KldMTLfbtJ__wYVBQ_4iTow?cn=THISLIFE&res=small",""
                print("Found a build-yourself comic, empty script and image_url")

            assert not stop

            filename = 'xkcd-' + page + '.png'
            item_dir = 'xkcd-' + page
            os.chdir(self.time)
            os.mkdir(item_dir)
            os.chdir(item_dir)

            # export to file
            image_path = os.path.join(self.time, item_dir, filename)
            comics_objs.append([index,Comic(page,title,script,image_url,comic_url,image_path)])

            if self.file_format == 'json':
                results = {'page': page, 'title': title, 'script': script, 'image_url': image_url, 'comic_url': comic_url}
                with open('xkcd-' + page + '.json', 'w') as f:
                    json.dump(results, f)
            elif self.file_format == 'csv':
                with open('xkcd-' + page + '.csv', 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['page', 'title', 'script', 'image_url','comic_url'])
                    writer.writerow([page, title, script, image_url,comic_url])
            else:
                raise KeyError(self.file_format+"isn't a supported format")
            os.chdir("..\\")
            os.chdir("..\\")
            assert not stop
            return scrapy.Request(url=image_url, callback=self.parse_img, cb_kwargs=dict(filename=filename,item_dir=item_dir))

        def parse_img(self, response, filename,item_dir):
            os.chdir(self.time)
            os.chdir(item_dir)
            with open(filename, 'wb') as f:
                f.write(response.body)
            self.log(f'Saved file {filename}')
            os.chdir("..\\")
            os.chdir("..\\")
            assert not stop

    process = CrawlerProcess()
    process.crawl(XKCDSpider,user_input=user_input, file_format=file_format, save_path=save_path)
    process.start()

    for var_ in ['pages','titles','scripts','comics','image_urls','comic_urls','image_paths']:
        exec(f'comics_objs.{var_}.sort(key=operator.itemgetter(0))')
        exec(f'for list_ in comics_objs.{var_} :\n del list_[0]')
        exec(f'comics_objs.{var_} = [list_[0] for list_ in comics_objs.{var_}]')
        assert not stop

    return comics_objs


if __name__ == "__main__":
    print(crawl(user_input='1,3,5-10,25',file_format="json").titles)
