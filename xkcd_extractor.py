import operator
import spider

def crawl(user_input, file_format='json', save_path="."):
    """
    mode : list, must define the :param 'list_' with a list
    mode : range, must define the :param 'start' and the :param 'end' with integers
    :param file_format , by default 'json' ,can be changed to 'csv'
    :param save_path , in working directory by default, can by change by a str path
    """
    # list to collect all items
    comics_objs = spider.sspider(user_input,save_path,file_format)
    for var_ in ['titles','comics','image_urls']:
        exec(f'comics_objs.{var_}.sort(key=operator.itemgetter(0))')
        exec(f'for list_ in comics_objs.{var_} :\n del list_[0]')
        exec(f'comics_objs.{var_} = [list_[0] for list_ in comics_objs.{var_}]')


    return comics_objs

if __name__ == "__main__":

    print(crawl(user_input='1,3,1100-*',file_format="json").titles)