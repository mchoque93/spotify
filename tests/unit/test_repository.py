from unittest.mock import patch, MagicMock

import pytest

from models.artist import Artist
from models.genre import Genre
from spotify_repository.repository import SpotifyRepository


class Test:
    @pytest.fixture
    def client_mock(self):
        return MagicMock()

    @pytest.fixture
    def repository(self, client_mock):
        return SpotifyRepository(client=client_mock)

    def test_get_top_artists(self, repository, client_mock):
        client_mock.get.return_value = {'items': [
            {'genres': ['reggaeton', 'trap latino', 'urbano latino'],
             'name': 'Bad Bunny'}]}
        top_artists = repository.get_top_artists(1)
        assert len(top_artists) == 1
        assert top_artists == [Artist(name='Bad Bunny', genres=['reggaeton', 'trap latino', 'urbano latino'])]

    def test_get_top_genres(self, repository):
        mock = MagicMock()
        repository.get_top_artists = mock
        mock.return_value = [Artist(name='Bad Bunny', genres=['reggaeton', 'trap latino', 'urbano latino'])]
        assert repository.get_top_genres() == [Genre(genre='reggaeton'), Genre(genre='trap latino'),
                                               Genre(genre='urbano latino')]
