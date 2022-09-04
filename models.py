from typing import Union
from pydantic import BaseModel

class Song(BaseModel):
    song_name: str
    artist_name: str
    track_link: str
    image: Union[str, None] = None
    danceability: Union[float, None] = None
    key: str
    tempo: Union[float, None] = None
    time_signature: Union[int, None] = None
    