from bs4 import BeautifulSoup
import requests
import re

def get_artist_relevance(artist_name):
    # TODO more sources of relevance? active touring? band disbanded?

    url = 'https://www.last.fm/music/' + artist_name.replace(' ', '+')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    metadata = soup.find('span', class_='metadata_column')
    metadata = metadata.find_all('catalogue-metadata-heading')
    for heading in metadata:
        if heading.text == 'Died':
            return False
    return True