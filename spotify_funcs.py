import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import credentials

spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=credentials.CLIENT_ID, client_secret=credentials.CLIENT_SECRET
    )
)


# results = spotify.artist_top_tracks(lz_uri)

# for track in results["tracks"][:10]:
#     print("track    : " + track["name"])
#     print("audio    : " + track["preview_url"])
#     print("cover art: " + track["album"]["images"][0]["url"])
#     print()

#     print(track)
#     print()


def get_song_id(song: str, artist: str):

    results = spotify.search(
        q="track:" + song + ", artist:" + artist, type="track"
    )
    songs = results["tracks"]

    return songs["items"][0]["id"]


# print(spotify.audio_features(get_song_id("karma police", "radiohead"))[0])

# print(spotify.track(get_song_id("karma police", "radiohead")))

# print(get_song_id("roundabout", "yes"))