from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import uvicorn
import credentials
import modules.spotify_funcs as spotify_funcs
import models.models as models
import modules.flash as flash


app = FastAPI(middleware=[Middleware(SessionMiddleware, secret_key='super-secret')])

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")
templates.env.globals['get_flashed_messages'] = flash.get_flashed_messages


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
async def post_home(
    request: Request, 
    song_query: str = Form(...), 
    artist_query: str = Form(...)
):
    try:
        song_id = spotify_funcs.get_song_id(song_query, artist_query)
        return RedirectResponse(url=f"/song/{song_id}", status_code=303)
    except: 
        flash.flash(request, "Song does not exist", "danger")
        return templates.TemplateResponse("index.html", {"request": request})
        

@app.get("/song/{song_id}")
async def get_song(request: Request, song_id: str):
    track = spotify.track(song_id)
    song_name = track["name"]
    artist_name = track["artists"][0]["name"]
    song_link = track["external_urls"]["spotify"]
    cover_art = track["album"]["images"][0]["url"]

    audio_features = spotify.audio_features(song_id)[0]
    key = audio_features["key"]
    tempo = audio_features["tempo"]
    time_signature = audio_features["time_signature"]
    acousticness = audio_features["acousticness"]
    danceability = audio_features["danceability"]
    energy = audio_features["energy"]
    instrumentalness = audio_features["instrumentalness"]
    liveness = audio_features["liveness"]
    valence = audio_features["valence"]

    song = models.Song(
        song_name=song_name,
        artist_name=artist_name,
        track_link=song_link,
        image=cover_art,
        key=spotify_funcs.translate_key(int(key)),
        tempo=tempo,
        time_signature=time_signature,
        acousticness=acousticness,
        danceability=danceability,
        energy=energy,
        instrumentalness=instrumentalness,
        liveness=liveness,
        valence=valence,
    )
    return templates.TemplateResponse("song.html", {"request": request, "song": song})


if __name__ == "__main__":
    uvicorn.run(app)
