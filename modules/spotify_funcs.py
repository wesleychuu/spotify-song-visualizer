import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=os.environ.get("SPOTIFY_CLIENT_ID"), client_secret=os.environ.get("SPOTIFY_CLIENT_SECRET")
    )
)


def get_song_id(song: str, artist: str):
    results = spotify.search(
        q="track:" + song + ", artist:" + artist, type="track"
    )
    songs = results["tracks"]

    return songs["items"][0]["id"]


def translate_key(key: int):
    key_dict = {
        -1: "None",
        0: "C",
        1: "C♯/D♭",
        2: "D",
        3: "D♯/E♭",
        4: "E",
        5: "F",
        6: "F♯/G♭",
        7: "G",
        8: "G♯/A♭",
        9: "A",
        10: "A♯/B♭",
        11: "B"
    }

    if key > 11 or key < -1:
        return ValueError
    else:
        return key_dict.get(key)

