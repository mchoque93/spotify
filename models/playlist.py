from dataclasses import dataclass

@dataclass
class Playlist:
    disco: str
    number_followers: int
    tempo: int
    acousticness: int
    danceability: int
    energy: int
    instrumentalness: int
    liveness: int
    loudness: int
    valence: int

