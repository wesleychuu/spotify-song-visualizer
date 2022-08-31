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

song_name = "Karma Police"
artist_name = "Radiohead"

results = spotify.search(
    q="track:" + song_name + ", artist:" + artist_name, type="track", limit=1
)
songs = results["tracks"]

print(songs["items"][0]["id"])

# if len(items) > 0:
#     artist = items[0]
#     print(artist["name"], artist["images"][0]["url"])