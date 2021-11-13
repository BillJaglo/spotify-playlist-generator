import requests
from bs4 import BeautifulSoup
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth


# get the date from the user and save a new variable with the top 100 url using the user's date chosen
date_chosen = input("What date would you like to travel to? Type the date in this format YYYY-MM-DD: ")
top_100_url = f"https://www.billboard.com/charts/hot-100/{date_chosen}"

# pull in the html on the billboard website and save into a new variable
response = requests.get(top_100_url)
top_100_html = response.text

# create soup with the top 100 html
# create a new list that pulls in the text of the title for each song during that date
soup = BeautifulSoup(top_100_html, "html.parser")
list_of_song_titles = [song.getText() for song in soup.find_all(name="span", class_="chart-element__information__song")]


# environment variables were created using the API credentials given by Spotify on the Spotify app
# create two variables pulling in the required API information saved as environment variables
spotify_client_id = os.environ.get("SPOTIPY_CLIENT_ID")
spotify_client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")

# use spotipy module to tap into the Spofity API
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=spotify_client_id,
        client_secret=spotify_client_secret,
        show_dialog=True,
        cache_path="token.txt"

    )
)
user_id = sp.current_user()["id"]

# create list of song uris for each song in the billboard top 100 list
song_uris = []
year_chosen = date_chosen.split("-")[0]
for song in list_of_song_titles:
    result = sp.search(q=f"track:{song} year:{year_chosen}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# create a playlist of songs that includes all of the song uris in the step above
playlist = sp.user_playlist_create(user=user_id, name=f"{date_chosen} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

