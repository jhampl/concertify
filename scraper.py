import requests
import spotipy
from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from helpers import event_fields, artist_fields
from datetime import datetime
from spotipy.oauth2 import SpotifyOAuth
from storage import add_artists, add_events
from configparser import ConfigParser


config = ConfigParser()
config.read('config.ini')
client_id = config.get('auth', 'SPOTIPY_CLIENT_ID')
client_secret = config.get('auth', 'SPOTIPY_CLIENT_SECRET')
redirect_uri = config.get('auth', 'SPOTIPY_REDIRECT_URI')
user_country = config.get('location', 'country')


if user_country:
    quote_plus(user_country.lower())


def update_all():
    artists = get_artists()
    for i, artist in enumerate(artists):
        print(
            f"{i+1}/{len(artists)}  Checking if {artist['name']} is active...")
        artist['active'] = is_artist_active(artist['name'])
    print('Storing artists...')
    add_artists(artists)

    print('Getting events...')
    for artist in artists:
        if artist['active']:
            events = get_events(artist)
            if events:
                print(f"Found Event! Storing events for {artist['name']}...")
                add_events(events)
    print('Done!')


# add active and ignore fields to artist
def artist_map(artist): return dict(
    zip(artist_fields, [artist['id'], artist['name'], True, False]))


def get_artists():
    scope = "user-follow-read"

    # Authorization flow
    if client_id and client_secret and redirect_uri:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))
    else:
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

    url = 'https://www.last.fm/music/' + artist_name.replace(' ', '+')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    metadata = soup.find_all(
        'dt', attrs={'class': 'catalogue-metadata-heading'})
    for heading in metadata:
        if heading.text.lower() == 'died':
            return False
        if heading.text.lower() == 'years active' and 'present' not in heading.find_next_sibling().text.lower():
            return False
    return True


def get_events(artist):

    artist_name = quote_plus(artist['name'])
    url = "https://www.songkick.com/search?page=1&per_page=10&query=" + \
        artist_name + f"+{user_country}&type=upcoming"
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    parsed_html = BeautifulSoup(html, features="html.parser")
    events_html = parsed_html.find_all(class_='concert event')
    parsed_events = []

    for event_html in events_html:
        event_data = {}

        # get event name
        try:
            summary = event_html.find('p', class_='summary')
            if summary:
                event_name = summary.text.strip()
            else:
                event_name = ''
        except:
            event_name = ''
        event_data['name'] = event_name
        
        # if artist name is not fully contained, considered false positive
        if event_name and artist['name'].lower() not in event_name.lower():
            continue

        # get artist id
        event_data['artist_id'] = artist['spotify_id']

        # get event date
        try:
            date = event_html.find('time').get('datetime')
            # remove time from date (unreliable data from songkick)
            date = datetime.strptime(date.split('T')[0], "%Y-%m-%d")
            # date = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S%z")
        except:
            date = ''
        event_data['date'] = date

        # get event location
        try:
            location = event_html.find('p', class_='location').text.strip()
        except:
            location = ''
        event_data['location'] = location

        # get event url
        try:
            url = 'https://www.songkick.com/' + \
                event_html.find(class_='actions').find('a').get('href')
        except:
            url = ''
        event_data['url'] = url

        event_data['dismissed'] = 0

        parsed_events.append(event_data)

    return parsed_events

