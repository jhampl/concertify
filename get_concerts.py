from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from helpers import event_fields, artist_fields
from datetime import datetime 


def get_concerts(artist_name):

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

res = get_concerts('Mitski')
print(res)