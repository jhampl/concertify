# Concertify
Python script that continuously informs you about upcoming concerts based on followed Spotify artists.
#### Video Presentation: [here](https://youtu.be/hG3QwGJxPEs)

#### Requirements:
- Windows 10
- Python3
- Spotify Account

#### Installation:
- Download the repo with `git clone`
- Create a Spotify app as described [here](https://developer.spotify.com/documentation/web-api/concepts/apps)
- Set the redirect URI to `http://localhost:8080`
- Add the received **Client_Id**, **_Secret** along with the **Redirect_URI** to `config.ini`
    - Alternatively, set them as **environment variables** using 
        -`SetX SPOTIPY_CLIENT_ID "xxx"` 
        -`SetX SPOTIPY_CLIENT_SECRET "xxx"`
        -`SetX SPOTIPY_REDIRECT_URI "xxx"`
- Set your country in `config.ini`
- Log into your Spotify Account on first launch and allow the app to access your followed artists
- install dependencies with with `pip install 'requirements.txt'`

#### Running Concertify
Start the app from the terminal with `python concertify.py`.

Concertify will search for events in the background and notify you when new ones are found.
It will update every 12 hours.
