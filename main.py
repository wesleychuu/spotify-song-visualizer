from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import credentials
import spotify_funcs

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=credentials.CLIENT_ID, client_secret=credentials.CLIENT_SECRET
    )
)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/{song_id}")
async def visualize_song(song_id):
    return spotify.audio_features(song_id)
