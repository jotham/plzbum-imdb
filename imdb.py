#!/usr/bin/python3
import re
import requests

IMDB_URL_PATTERN = r'https://www\.imdb\.com/title/([a-zA-Z0-9]+)/?'
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'}

def get_imdb_title(imdb_id):
    url = 'https://www.imdb.com/title/{}/'.format(imdb_id)
    response = requests.get(url, headers=HEADERS)
    match = re.search(r'og:title" content="([^"]+)"', response.text)
    if match:
        return match.group(1).split(' | ')[0]
    return None

try:
    import sopel.module
except ImportError:
    pass
else:
    @sopel.module.rule(r'.*' + IMDB_URL_PATTERN + r'.*')
    def f_imdb(bot, trigger):
        match = re.search(IMDB_URL_PATTERN, trigger.group(0))
        if match:
            title = get_imdb_title(match.group(1))
            if title:
                bot.say(title)

if __name__ == '__main__':
    import sys
    imdb_id = 'tt4359416'
    if len(sys.argv) > 1:
        imdb_id = sys.argv[1]
    print('Looking up "{}"'.format(imdb_id))
    title = get_imdb_title(imdb_id)
    if title:
        print(title)
    else:
        print('Could not find title for {}'.format(imdb_id))
