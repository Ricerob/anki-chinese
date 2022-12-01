from bs4 import BeautifulSoup
from requests import get
import argparse

def collect_zh_chars(entry):
    zh_chars = []
    char_anchor_list = entry.findChildren("a", recursive=True)
    for char in char_anchor_list:
        if char.has_attr('class'):
            continue
        zh_chars.append(char.get_text())

    return ''.join(zh_chars)


def grab_en_def(entry):
    def_list = entry.findChildren("div", {'class': 'meaning'}, recursive=True)
    definition = ''

    for defin in def_list:
        definition += defin.get_text()

    return definition

def grab_audio_link(entry):
    audio_link_entry = entry.find("i", {'class': 'word_audio'})
    return audio_link_entry['data-audio_url']

def content_scraper(phrase):
    url = 'https://chinese.yabla.com/chinese-english-pinyin-dictionary.php?define=' + str(phrase)
    res = get(url).text
    soup = BeautifulSoup(res, 'html.parser')
    translate_list = soup.find_all('li', {'class': 'entry'})

    if len(translate_list) == 0:
        print('No translations found. Try another term.')
        exit(0)

    content = []

    for entry in translate_list:
        entry_content = []
        entry_content.append({'zh', collect_zh_chars(entry)})
        entry_content.append({'pinyin', entry.findNext('span', {'class': 'pinyin'}).get_text()})
        entry_content.append({'english', grab_en_def(entry)})
        entry_content.append({'audio_link', grab_audio_link(entry)})
        content.append(entry_content)

    return content


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="anki-zh-card-creator",
        description="Creates an Anki card based on input"
    )

    parser.add_argument('input', help='Input word/ phrase. Surround with quotes or escape spaces.')

    args = vars(parser.parse_args())

    phrase = args['input']
    phrase = phrase.replace(" ", "+")

    content = content_scraper(phrase)

    if len(content) > 1:
        print("Multiple translations found, picking the top result.")

    print(content[0])
