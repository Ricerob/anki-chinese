from bs4 import BeautifulSoup
from requests import get
import argparse

def content_scraper(phrase, input_type):
    url = 'https://chinese.yabla.com/chinese-english-pinyin-dictionary.php?define=' + str(phrase)
    res = get(url).text
    soup = BeautifulSoup(res, 'html.parser')
    translate_list = soup.find_all('li', {'class': 'entry'})

    if len(translate_list) == 0:
        print('No translations found. Try another term.')
        exit(0)

    content = []

    if input_type == 'zh' or input_type == 'pi':
        for entry in translate_list:
            entry_content = []
            entry_content.append({'zh', entry.find})

    return translate_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="anki-zh-card-creator",
        description="Creates an Anki card based on input"
    )

    parser.add_argument('-i', '--inputtype',
                        choices=['zh', 'en', 'pi'], required=True,
                        help='Input language/ character system. \'zh\' for Chinese characters, \'en\' for English, '
                             '\'pi\' for pinyin (include tone markers).')
    parser.add_argument('input', help='Input word/ phrase. Surround with quotes or escape spaces.')

    args = vars(parser.parse_args())

    input_type = args['inputtype']
    phrase = args['input']
    phrase = phrase.replace(" ", "+")

    content = content_scraper(phrase, input_type)
