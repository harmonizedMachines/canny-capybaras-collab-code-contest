import spider
import operator
from spider import SucideSpider
from scrapy.crawler import CrawlerProcess

def crawl(user_input, file_format='json', save_path="."):
    """
    mode : list, must define the :param 'list_' with a list
    mode : range, must define the :param 'start' and the :param 'end' with integers
    :param file_format , by default 'json' ,can be changed to 'csv'
    :param save_path , in working directory by default, can by change by a str path
    """
    # list to collect all items

    process = CrawlerProcess({
        'USER_AGENT': 'scrapy',
        'LOG_LEVEL': 'INFO',
        'ITEM_PIPELINES': {'__main__.ItemCollectorPipeline': 100}
    })

    # start the spider
    process.crawl(SucideSpider)
    process.start()
    if '*' in user_input:
        user_input = user_input.replace('*', items[0]['lastest_comic'])
    user_input = user_input.split(',')
    for index_input, input_ in enumerate(user_input):
        if '-' in input_:
            split_input = input_.split('-')
            str_range = [str(int_) for int_ in range(int(split_input[0]), int(split_input[1]) + 1)]
            user_input[index_input:index_input] = str_range
            user_input.remove(input_)
    user_input = [int(input_) for input_ in user_input]

    return spider.cspider(user_input,file_format,save_path)

if __name__ == "__main__":
    items = []

    # pipeline to fill the items list
    class ItemCollectorPipeline(object):
        def __init__(self):
            self.ids_seen = set()

        def process_item(self, item, spider):
            items.append(item)
    print(crawl(user_input='1,3,1100-*',file_format="json").titles)