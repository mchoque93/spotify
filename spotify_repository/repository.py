import statistics
from itertools import islice
from typing import List

from client import SpotifyClient
from config import BASE_URL
from models.artist import Artist
from models.song import Song
from collections import Counter

client = SpotifyClient()


class SpotifyRepository:
    def get_top_artists(self, limit=10) -> List['Artist']:
        response_json = client.get(BASE_URL + f"me/top/artists?limit={limit}")
        top_artists = [Artist(row['name'], row['genres']) for row in response_json['items']]
        return top_artists

    def get_top_tracks_by_user(self, limit=10) -> List['Song']:
        response_json = client.get(BASE_URL + f"me/top/tracks?limit={limit}")
        name_song = [row['name'] for row in response_json['items']]
        lista_artistas = [[item['name'] for item in row['album']['artists']] for row in response_json['items']]
        top_canciones = []
        for song, artists in zip(name_song, lista_artistas):
            top_canciones.append([Song(song, artists)])
        return top_canciones

    def get_top_genres(self) -> List:
        top_artistas = self.get_top_artists()
        generos = [genre for item in top_artistas for genre in item.genres]
        dic_generos = dict(Counter(generos))
        top_5 = list(islice(dic_generos.items(), 5))
        return [row[0] for row in top_5]

    def get_playlist(self, id: str):
        url_base = f"https://api.spotify.com/v1/playlists/{id}"
        cover = client.get(url_base + "/images")
        num_followers = client.get(url_base)['followers']['total']

        id_tracks = [row['track']['id'] for row in client.get(url_base + "/tracks")['items']]
        lista_tracks = []
        for id in id_tracks:
            url_tracks = client.get(f"https://api.spotify.com/v1/audio-features/{id}")
            lista_tracks.append(url_tracks)

        dic = {}
        for parametro in ['danceability', 'tempo', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'loudness', 'valence']:
            dic[parametro] = statistics.mean([row[parametro] for row in lista_tracks])
            print(dic)



