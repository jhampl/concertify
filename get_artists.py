import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-follow-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

results = sp.current_user_followed_artists(limit=50)
artnum = 0
while True:
    for i, item in enumerate(results['artists']['items']):
        artnum += 1
        print(artnum, i, item['name'])
    if not results['artists']['next']:
        break
    results = sp.next(results['artists'])


#for idx, item in enumerate(results['items']):
#    track = item['track']
#    print(idx, track['artists'][0]['name'], " – ", track['name'])