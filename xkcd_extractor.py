import operator
from spider import sspider,cspider

def crawl(user_input, file_format='json', save_path="."):
    """
    mode : list, must define the :param 'list_' with a list
    mode : range, must define the :param 'start' and the :param 'end' with integers
    :param file_format , by default 'json' ,can be changed to 'csv'
    :param save_path , in working directory by default, can by change by a str path
    """
    # list to collect all items

    lastest_comic = sspider()
    if '*' in user_input:
        user_input = user_input.replace('*', lastest_comic)
    user_input = user_input.split(',')
    for index_input, input_ in enumerate(user_input):
        if '-' in input_:
            split_input = input_.split('-')
            str_range = [str(int_) for int_ in range(int(split_input[0]), int(split_input[1]) + 1)]
            user_input[index_input:index_input] = str_range
            user_input.remove(input_)
    user_input = [int(input_) for input_ in user_input]

    comics_objs = cspider(user_input,save_path,file_format)
    for var_ in ['titles','comics','image_urls']:
        exec(f'comics_objs.{var_}.sort(key=operator.itemgetter(0))')
        exec(f'for list_ in comics_objs.{var_} :\n del list_[0]')
        exec(f'comics_objs.{var_} = [list_[0] for list_ in comics_objs.{var_}]')


    return comics_objs

if __name__ == "__main__":

    print(crawl(user_input='1,3,1100-*',file_format="json").titles)