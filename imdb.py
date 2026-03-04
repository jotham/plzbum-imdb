#!/usr/bin/python3
import re
import requests

IMDB_URL_PATTERN = r'https://www\.imdb\.com/title/([a-zA-Z0-9]+)/?'
OMDB_URL = 'https://www.omdbapi.com/'

def get_omdb_info(imdb_id, api_key):
    response = requests.get(OMDB_URL, params={'i': imdb_id, 'apikey': api_key})
    if response.status_code != 200:
        return None
    data = response.json()
    if data.get('Response') == 'False':
        return None
    return data

def format_title(data):
    parts = [data.get('Title', 'Unknown')]
    year = data.get('Year')
    if year:
        parts[0] += ' ({})'.format(year)
    media_type = data.get('Type', '').capitalize()
    if media_type:
        parts.append(media_type)
    rating = data.get('imdbRating')
    if rating and rating != 'N/A':
        parts.append('IMDB: {}/10'.format(rating))
    votes = data.get('imdbVotes')
    if votes and votes != 'N/A':
        parts.append('{} votes'.format(votes))
    genre = data.get('Genre')
    if genre and genre != 'N/A':
        parts.append(genre)
    return ' | '.join(parts)

try:
    import sopel.module
except ImportError:
    pass
else:
    @sopel.module.rule(r'.*' + IMDB_URL_PATTERN + r'.*')
    def f_imdb(bot, trigger):
        api_key = bot.config.plzbum_imdb.api_key
        match = re.search(IMDB_URL_PATTERN, trigger.group(0))
        if match:
            data = get_omdb_info(match.group(1), api_key)
            if data:
                bot.say(format_title(data))

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print('Usage: imdb.py <omdb api_key> <imdb_id>')
    else:
        api_key = sys.argv[1]
        imdb_id = sys.argv[2]
        print('Looking up "{}"'.format(imdb_id))
        data = get_omdb_info(imdb_id, api_key)
        if data:
            print(format_title(data))
        else:
            print('Could not find info for {}'.format(imdb_id))
