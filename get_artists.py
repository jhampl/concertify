import spotipy
from spotipy.oauth2 import SpotifyOAuth

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