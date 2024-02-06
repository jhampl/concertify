# Concertify
Python script that continuously informs you about upcoming concerts based on followed Spotify artists.
#### Video Presentation:
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/hG3QwGJxPEs/0.jpg)](https://www.youtube.com/watch?v=hG3QwGJxPEs)

## Requirements:
- Windows 10
- Python3
- Spotify Account

## Installation:
- Download the repo with 
```bash
git clone https://github.com/jhampl/concertify.git
```
- Create a Spotify app as described in the [Spotify Documentation](https://developer.spotify.com/documentation/web-api/concepts/apps)
- Set the redirect URI to `http://localhost:8080`
- Add the received **Client_Id**, **_Secret** along with the **Redirect_URI** to `config.ini`
    - Alternatively, set them as **environment variables** using:
        - `SetX SPOTIPY_CLIENT_ID "xxx"` 
        - `SetX SPOTIPY_CLIENT_SECRET "xxx"`
        - `SetX SPOTIPY_REDIRECT_URI "xxx"`
- Set your country in `config.ini`
- Log into your Spotify Account on first launch and allow the app to access your followed artists
- install dependencies with with 
```bash
pip install -r 'requirements.txt'
```

## Running Concertify
Start the app from the terminal in the root directory of the app with `python concertify.py`.

Concertify will search for events in the background and notify you when new ones are found.
<br>It will update every 12 hours.

## Details
### Spotify API calls with spotipy

#### Spotify Artists Fetching
- Spotify Artists are fetched using the Spotify API Wrapper [spotipy](https://github.com/spotipy-dev/spotipy).
- The application authenticates with Spotify using the Spotify Authorization Code Flow implementation of spotipy
- On the first run, spotipy hosts a webpage on the `SPOTIPY_REDIRECT_URI` to prompt the user to log in and authenticate the app for the `user_followed_artists` scope.
- The application then creates a `.cache` file containing an access token and refresh token, enabling spotipy to refresh the token without requiring the user to log in again. Refer to the [Spotify API Documentation](https://developer.spotify.com/documentation/web-api/tutorials/code-flow) for more details.

### Data Scraping

#### Artist Data
- All followed artists are fetched from Spotify.
- The active status of each artist is confirmed using [last.fm](www.last.fm), filtering out disbanded bands and deceased artists.
- Active artists are then passed to the event scraper.

#### Event Scraper
- The event scraper crawls [songkick.com](www.songkick.com) to find new events in the country specified in the `config.ini` file.
- To minimize false matches, the event name is required to contain the full artist name, though false matches may still occur, as songkick.com does not handle spotify ids.
- Both artists and events are stored in an SQLite database for efficient data management.

### Local Web App

#### Notification System
- When events are found, Concertify sends a Windows system notification using [winotify](https://github.com/versa-syahptr/winotify), displaying the count of new events.
- Clicking on the notification opens a locally hosted web interface.

#### Local Web Interface
- A lightweight web server runs as a daemon at startup, serving a simple web interface to the user.
- The interface queries the database for events that the user hasn't dismissed and that lie in the future.
- [Jinja2](https://jinja.palletsprojects.com/) is used to generate HTML from a template, creating a table of events.
- Concertify generates Google Calendar links, enabling users to add events to their calendars.
- Users can dismiss events with a button that sends a post request to the web server, marking them as dismissed in the database to prevent further display.

#### Update Mechanism
- Concertify updates every 12 hours, writing a current timestamp into the `LASTUPDATE` file after successfully fetching events.
- The application checks every hour whether 12 hours have passed, ensuring regular updates and limit resource use.

## Database

#### Artists Table
- spotify_id 
- name 
- active: A boolean indicating whether the artist is currently active. Default is set to TRUE.
- ignored: A boolean indicating whether the artist is ignored. Default is set to FALSE.

```sql
Copy code
CREATE TABLE artists (
    spotify_id VARCHAR PRIMARY KEY,
    name VARCHAR,
    active BOOL DEFAULT TRUE,
    ignored BOOL DEFAULT FALSE
);
```

#### Events Table
- id
- name
- location: location string read as-is from songkick.com event, usually contains venue, city, country
- artist_id
- date: event date with format `%Y-%M-%dT%H:%M:%S%`, time is set to `00:00:00` as current data source is unreliable
- url: songkick.com URL of the event
- dismissed: A boolean indicating whether the event notification has been dismissed. Default is set to FALSE.

```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    name VARCHAR,
    location VARCHAR,
    artist_id INTEGER,
    date DATETIME,
    url VARCHAR,
    dismissed BOOL DEFAULT FALSE,
    FOREIGN KEY (artist_id) REFERENCES artists(spotify_id)
);
```
#### Unique Indices
```sql
CREATE UNIQUE INDEX ux_artists ON artists (name, spotify_id, active);
CREATE UNIQUE INDEX ux_events ON events (artist_id, date, location);
```
