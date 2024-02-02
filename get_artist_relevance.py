from bs4 import BeautifulSoup
import requests

def get_artist_relevance(artist_name):

    url = 'https://www.last.fm/music/' + artist_name.replace(' ', '+')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    metadata = soup.find_all('dt', attrs={'class':'catalogue-metadata-heading'})
    for heading in metadata:
        if heading.text.lower() == 'died':
            return False
        if heading.text.lower() == 'years active':
            return False
    return True

print(get_artist_relevance('The Beatles'))