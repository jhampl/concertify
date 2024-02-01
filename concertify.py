from get_artists import get_artists
from get_artist_relevance import get_artist_relevance
from get_concerts import get_concerts
import storage
import socketserver
import http.server
import notify.notify as notify

def main():
    print("Authenticating...")
    
    print("Getting artists...")
    artists = get_artists.get_artists()
    for artist in artists:
        artist['relevance'] = get_artist_relevance(artist['name'])
    storage.store_artists(artists)
    # TODO store in batches of 50, because of spotify api limit, change get_artists
    concerts = get_concerts(artists)
    # TODO add notified field to concerts
    
    # TODO alert
    notify(concerts)


DIRECTORY = './page'
class ConcertifyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    cgi_directories = ['./page/cgi-bin']

    def do_POST(self):
        # TODO get headers and add artist to ignore
        self.send_response(303)
        self.send_header('Location','/')
        self.end_headers()

        message = "Hello, World! Here is a POST response"
        #self.wfile.write(bytes(message, "utf8"))

def start_webserver():
    PORT = 8080

    with socketserver.TCPServer(("", PORT), ConcertifyRequestHandler) as httpd:
        print(f"Server started at http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    main()