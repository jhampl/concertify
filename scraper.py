from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from helpers import event_fields, artist_fields
from datetime import datetime 
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from storage import update_artists, update_events

def update_all():
    artists = get_artists()
    for artist in artists:
        events = get_events(artist['name'])
        # TODO store events in db
        
def get_artists():
    # TODO return in batches of 50
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

def get_events(artist_name):

    artist_name = quote_plus(artist_name)
    url = "https://www.songkick.com/search?page=1&per_page=10&query=" + artist_name + "+germany&type=upcoming"
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    parsed_html = BeautifulSoup(html, features="html.parser")
    events_html = parsed_html(class_='concert event')
    parsed_events = []

    for event_html in events_html:
        event_details = []

        # get event name
        try:
            summary = event_html.find('p', class_='summary').text.split(',')
            if len(summary) >= 2:
                event_details.append(summary[-1])
        except:
            event_details.append('')

        # get event date
        try:
            time = event_html.find('p', class_='time').get('datetime')
            time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S%z")
        except:
            event_details.append('')
        
        # get event location
        try:
            event_details.append(event_html.find('p', class_='location').text)
        except:
            event_details.append('')

        # get event url
        try:
            event_details.append(event_html.find(class_='actions').find('a').get('href'))
        except:
            event_details.append('')

        # set notified to false
        event_details.append(False)

        # create event dict
        parsed_events.append(dict(zip(event_fields, event_details)))

    return parsed_events
