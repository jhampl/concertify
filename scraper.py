from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup, NavigableString
from urllib3 import request
from helpers import event_fields, artist_fields
from datetime import datetime 
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from storage import add_artists, add_events

def update_all():
    artists = get_artists()
    for artist in artists:
        artist['active'] = is_artist_active(artist['name'])
    add_artists(artists)

    for artist in artists:
        if artist['active']:
            events = get_events(artist)
            add_events(events)
    

artist_map = lambda artist: dict(zip(artist_fields, [artist['id'], artist['name'], True, False]))

def get_artists():
    scope = "user-follow-read"

    # Authorization flow
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    results = sp.current_user_followed_artists(limit=50)
    artists = []
    while True:
        artists.extend(results['artists']['items'])

        if not results['artists']['next']:
            break

        results = sp.next(results['artists'])
    
    
    artists = filter(lambda artist: artist['type'] == 'artist', artists)
    artists = map(artist_map, artists)
    artists = list(artists)
    return artists

def is_artist_active(artist_name):

    url = 'https://www.last.fm/music/' + quote_plus(artist_name.replace)
    response = request.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    metadata = soup.find_all('dt', attrs={'class':'catalogue-metadata-heading'})
    for heading in metadata:
        if heading.text.lower() == 'died':
            return False
        if heading.text.lower() == 'years active':
            return False
    return True

def get_events(artist):

    artist_name = quote_plus(artist['name'])
    url = "https://www.songkick.com/search?page=1&per_page=10&query=" + artist_name + "+germany&type=upcoming"
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    parsed_html = BeautifulSoup(html, features="html.parser")
    events_html = parsed_html.find_all(class_='concert event')
    parsed_events = []

    for event_html in events_html:
        event_values = []

        # get artist id
        event_values.append(artist['id'])

        # get event name
        try:
            summary = event_html.find('p', class_='summary')
            if summary:
                event_values.append(summary.text.strip())
            else:
                event_values.append('')
        except:
            event_values.append('')

        # get event date
        try:
            time = event_html.find('time').get('datetime')
            # remove time from date
            time = datetime.strptime(time.split('T')[0], "%Y-%m-%d")
            event_values.append(time)
            # time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S%z")
        except:
            event_values.append('')
        
        # get event location
        try:
            event_values.append(event_html.find('p', class_='location').text.strip())
        except:
            event_values.append('')

        # get event url
        try:
            event_values.append('https://www.songkick.com/' + event_html.find(class_='actions').find('a').get('href'))
        except:
            event_values.append('')

        # set notified to false
        event_values.append(False)

        # create event dict
        parsed_events.append(dict(zip(event_fields, event_values)))

    return parsed_events

if __name__ == '__main__':
    artists = get_artists()
    for artist in artists[:5]:
        events = get_events(artist['name'])
        print(events)
    print(get_events('Thundercat'))