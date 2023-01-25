from services.save_csv import save_csv
from spotify_repository.repository import SpotifyRepository

if __name__ == '__main__':
    repository = SpotifyRepository()
    top_canciones_artistas = repository.get_top_tracks_by_user(10)
    save_csv("top_canciones_artistas", top_canciones_artistas)

    top_artistas = repository.get_top_artists(10)
    save_csv("top_artistas", top_artistas)

    top_genres = repository.get_top_genres()
    save_csv("top_genres", top_genres)

    playlist = repository.get_playlist("37i9dQZF1DWWGFQLoP9qlv")
    save_csv("playlist", playlist)

