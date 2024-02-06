import socketserver
import http.server
from jinja2 import Environment, FileSystemLoader, select_autoescape
import urllib.parse
from storage import get_new_relevant_events, dismiss_event, get_artist_name
from datetime import datetime


def generate_calendar_link(event):
    base_url = "https://www.google.com/calendar/render"
    date = datetime.fromisoformat(event["date"]).strftime("%Y%m%d")
    params = {
        "action": "TEMPLATE",
        "dates": date + "/" + date,
        "text": get_artist_name(event["artist_id"]),
        "details": event["name"],
        "location": event["location"]
    }
    encoded_params = urllib.parse.urlencode(params)
    calendar_link = f"{base_url}?{encoded_params}"
    return calendar_link


def format_date(date):
    return datetime.fromisoformat(date).strftime("%d/%m/%Y")


env = Environment(
    loader=FileSystemLoader("server/templates/"),
    autoescape=select_autoescape()
)
env.globals.update(
    generate_calendar_link=generate_calendar_link, format_date=format_date)
template = env.get_template('index.html')

DIRECTORY = './'


class ConcertifyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        events = get_new_relevant_events()
        content = template.render(events=events)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(content, "utf8"))

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len).decode('utf8')
        if post_body and "event-id=" in post_body and "/n" not in post_body:
            event_id = post_body.split("=")[1]
            print(f"Dismissing event with id {event_id}")
            dismiss_event(event_id)

        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()


def start_webserver(port=8085):
    PORT = port

    try:
        with socketserver.TCPServer(("", PORT), ConcertifyRequestHandler) as server:
            print(
                f"Server started at http://localhost:{server.server_address[1]}")
            server.serve_forever()
    except:
        print("Shutting down the server")
        server.socket.close()
