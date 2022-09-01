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


@app.get("/song/{song_id}")
async def visualize_song(song_id):
    return spotify.audio_features(song_id)[0], spotify.track(song_id)


if __name__ == "__main__":
    uvicorn.run(app)