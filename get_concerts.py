from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://www.songkick.com/search?page=1&per_page=10&query=thundercat+germany&type=upcoming"
page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")
parsed_html = BeautifulSoup(html, features="html.parser")
events = parsed_html(class_='concert event')

for event in events:
    time = event.find('time').get('datetime')
    location = event.find(class_= 'location').text
    link = event.find(class_='actions').find('a').get('href')
    print(time, location, link, sep='\n')

