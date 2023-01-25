import statistics
from itertools import islice
from typing import List

from client import SpotifyClient
from config import BASE_URL
from models.artist import Artist
from models.genre import Genre
from models.playlist import Playlist
from models.song import Song
from collections import Counter


class SpotifyRepository:

    def __init__(self, client=None):
        self.client = client or SpotifyClient()

    def get_top_artists(self, limit=10) -> List['Artist']:
        response_json = self.client.get(BASE_URL + f"me/top/artists?limit={limit}")
        top_artists = [Artist(row['name'], row['genres']) for row in response_json['items']]
        return top_artists

    def get_top_tracks_by_user(self, limit=10) -> List['Song']:
        response_json = self.client.get(BASE_URL + f"me/top/tracks?limit={limit}")
        name_song = [row['name'] for row in response_json['items']]
        lista_artistas = [[item['name'] for item in row['album']['artists']] for row in response_json['items']]
        top_canciones = []
        for song, artists in zip(name_song, lista_artistas):
            top_canciones.append(Song(song, artists))
        return top_canciones

    def get_top_genres(self) -> List:
        top_artistas = self.get_top_artists()
        generos = [genre for item in top_artistas for genre in item.genres]
        dic_generos = dict(Counter(generos))
        top_5 = list(islice(dic_generos.items(), 5))
        return [Genre(row[0]) for row in top_5]

    def get_cover(self, url_base):
        cover = self.client.get(url_base + "/images")
        return cover

    def get_number_followers(self, url_base):
        num_followers = self.client.get(url_base)['followers']['total']
        return num_followers

    def get_id_tracks(self, url_base):
        id_tracks = [row['track']['id'] for row in self.client.get(url_base + "/tracks")['items']]
        lista_tracks = []
        for id in id_tracks:
            url_tracks = self.client.get(f"https://api.spotify.com/v1/audio-features/{id}")
            lista_tracks.append(url_tracks)
        return lista_tracks

    def get_stadistics(self, lista_id: List):
        dic = {}
        for parametro in ['danceability', 'tempo', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'loudness',
                          'valence']:
            dic[parametro] = statistics.mean([row[parametro] for row in lista_id])
        return dic

    def get_playlist(self, id: str) -> List["Playlist"]:
        url_base = f"https://api.spotify.com/v1/playlists/{id}"
        cover = self.get_cover(url_base)
        num_followers = self.get_number_followers(url_base)
        lista_id = self.get_id_tracks(url_base)
        dic_stats = self.get_stadistics(lista_id)

        playlist = [Playlist(disco=cover, number_followers=num_followers, tempo=dic_stats['tempo'],
                             acousticness=dic_stats['acousticness'],
                             danceability=dic_stats['danceability'], energy=dic_stats['energy'],
                             instrumentalness=dic_stats['instrumentalness'],
                             liveness=dic_stats['liveness'], loudness=dic_stats['loudness'],
                             valence=dic_stats['valence'])]
        return playlist
