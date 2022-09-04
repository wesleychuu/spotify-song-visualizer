from fastapi import FastAPI, Request, Form 
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import uvicorn
import credentials
import spotify_funcs
import models

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=credentials.CLIENT_ID, client_secret=credentials.CLIENT_SECRET
    )
)


@app.get("/")
async def redirect_home():
    return RedirectResponse("/home")


@app.get("/home", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/home", response_class=HTMLResponse)
async def post_home(request: Request, song_query: str = Form(...), artist_query: str = Form(...)):
    song_id = spotify_funcs.get_song_id(song_query, artist_query)
    return RedirectResponse(url=f"/song/{song_id}", status_code=303)


# @app.get("/song/{song_id}")
# async def visualize_song(song_id):
#     return spotify.audio_features(song_id)[0], spotify.track(song_id)

@app.get("/song/{song_id}")
async def get_song(request: Request, song_id: str):
    track = spotify.track(song_id)
    song_name = track['name']
    artist_name = track['artists'][0]['name']
    song_link = track['external_urls']['spotify']
    cover_art = track['album']['images'][0]['url']

    audio_features = spotify.audio_features(song_id)[0]
    danceability = audio_features['danceability']
    key = audio_features['key']
    tempo = audio_features['tempo']
    time_signature = audio_features['time_signature']

    song = models.Song(
        song_name=song_name, artist_name=artist_name, track_link=song_link, image=cover_art,
        danceability=danceability, key=spotify_funcs.translate_key(int(key)), tempo=tempo, time_signature=time_signature
    )
    return templates.TemplateResponse("song.html", {"request": request, "song": song})

if __name__ == "__main__":
    uvicorn.run(app)