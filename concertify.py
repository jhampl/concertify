from get_artists import get_artists
from get_artist_relevance import get_artist_relevance
from get_concerts import get_concerts
import store

def main():
    print("Authenticating...")
    
    print("Getting artists...")
    artists = get_artists.get_artists()
    for artist in artists:
        artist['relevance'] = get_artist_relevance(artist['name'])
    store.store_artists(artists)
    # TODO store in batches of 50, because of spotify api limit, change get_artists
    concerts = get_concerts(artists)
    # TODO add notified field to concerts
    
    # TODO alert
    # TODO make calendar events

if __name__ == "__main__":
    main()