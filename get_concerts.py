from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup


def get_concerts(artist_name):

    # TODO backoff factor, retry on failure
    # TODO allow for more sources, generalize code
    artist_name = quote_plus(artist_name)
    url = "https://www.songkick.com/search?page=1&per_page=10&query=" + artist_name + "+germany&type=upcoming"
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    parsed_html = BeautifulSoup(html, features="html.parser")
    events = parsed_html(class_='concert event')

    # TODO fix this and decide which way is more readable
    for event in events:
        # TODO match data order and count with event_fields
        time = event.find('time').get('datetime')
        location = event.find(class_= 'location').text
        link = event.find(class_='actions').find('a').get('href')
        events.add(zip(event_fields, event_details))
        {'time': time, 'location': location, 'link': link}

res = get_concerts('Herbert Grönemeyer')
print(res)