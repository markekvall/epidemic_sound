import unittest
from unittest.mock import Mock
from app.application.playlist_service import PlaylistService
from app.schemas.playlist_schema import PlaylistCreate, PlaylistCreateRequest, PlaylistsResponse

class TestPlaylistService(unittest.TestCase):
    def setUp(self):
        self.mock_repository = Mock()
        self.service = PlaylistService(self.mock_repository)

    def test_create_playlists(self):
        # IF
        mock_db = Mock()
        mock_playlist = Mock(id=1, title="Test Playlist", sounds=[Mock(id=1), Mock(id=2)])
        self.mock_repository.create_playlist.return_value = mock_playlist
        playlist_data = PlaylistCreateRequest(data=[PlaylistCreate(title="Test Playlist", sounds=[1, 2])])

        # WHEN
        result = self.service.create_playlists(mock_db, playlist_data)

        # THEN
        self.mock_repository.create_playlist.assert_called_once_with(mock_db, "Test Playlist", [1, 2])
        self.assertEqual(len(result.data), 1)
        self.assertEqual(result.data[0].id, 1)
        self.assertEqual(result.data[0].title, "Test Playlist")
        self.assertEqual(result.data[0].sounds, [1, 2])


    def test_get_playlists_by_sound_success(self):
        # IF
        mock_db = Mock()
        sound_id = 1
        mock_playlists = [
            Mock(id=10, title="Chill Vibes", sounds=[Mock(id=1), Mock(id=2)]),
            Mock(id=20, title="Workout Beats", sounds=[Mock(id=1), Mock(id=3)])
        ]
        self.mock_repository.get_by_sound_id.return_value = mock_playlists

        # WHEN
        result = self.service.get_playlists_by_sound(mock_db, sound_id)

        # THEN
        self.mock_repository.get_by_sound_id.assert_called_once_with(mock_db, sound_id)
        self.assertIsInstance(result, PlaylistsResponse)
        self.assertEqual(len(result.data), 2)
        self.assertEqual(result.data[0].id, 10)
        self.assertEqual(result.data[0].title, "Chill Vibes")
        self.assertEqual(result.data[0].sounds, [1, 2])
        self.assertEqual(result.data[1].id, 20)
        self.assertEqual(result.data[1].title, "Workout Beats")
        self.assertEqual(result.data[1].sounds, [1, 3])

if __name__ == '__main__':
    unittest.main()