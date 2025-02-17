import unittest
from unittest.mock import Mock
from app.application.sound_service import SoundService
from app.schemas.sound_schema import CreditCreate, SoundCreate, SoundData, SoundsResponse


class TestSoundService(unittest.TestCase):
    def setUp(self):
        self.mock_sound_repository = Mock()
        self.mock_playlist_repository = Mock()
        self.service = SoundService(self.mock_sound_repository, self.mock_playlist_repository)

    def test_create_sound(self):
        # IF
        mock_db = Mock()

        sound_data = SoundCreate(data=[
            SoundData(
                title="Test Sound",
                bpm=120,
                duration_in_seconds=180,
                genres=["Pop"],
                credits=[CreditCreate(name="Test Artist", role="VOCALIST")]
            )
        ])
        mock_genre = Mock()
        mock_genre.id = 1
        mock_genre.name = "Pop"

        mock_credit = Mock()
        mock_credit.id = 1
        mock_credit.name = "Test Artist"
        mock_credit.role = "VOCALIST"

        mock_sound = Mock(
            id=1,
            title="Test Sound",
            bpm=120,
            duration_in_seconds=180,
            genres=[mock_genre],
            credits=[mock_credit]
        )
        self.mock_sound_repository.get_by_name_and_artist.return_value = None
        self.mock_sound_repository.create_sound.return_value = mock_sound

        # WHEN
        result = self.service.create_sounds(mock_db, sound_data)

        # THEN
        self.assertIsInstance(result, SoundsResponse)
        self.assertEqual(len(result.data), 1)
        self.assertEqual(result.data[0].title, "Test Sound")
        self.assertEqual(result.data[0].bpm, 120)
        self.assertEqual(result.data[0].duration_in_seconds, 180)
        self.assertEqual(result.data[0].genres[0].id, 1) 
        self.assertEqual(result.data[0].genres[0].name, "Pop")
        self.assertEqual(result.data[0].credits[0].name, "Test Artist")


    def test_get_sounds(self):
        # IF
        mock_db = Mock()
        mock_genre = Mock()
        mock_genre.id = 1
        mock_genre.name = "Pop"
        mock_credit = Mock()
        mock_credit.id = 1
        mock_credit.name = "Test Artist"
        mock_credit.role = "VOCALIST"
        mock_sound = Mock(id=1, title="Test Sound", bpm=120, duration_in_seconds=180, genres=[mock_genre], credits=[mock_credit])
        self.mock_sound_repository.get_all.return_value = [mock_sound]

        # WHEN
        result = self.service.get_sounds(mock_db)

        # THEN
        self.assertIsInstance(result, SoundsResponse)
        self.assertEqual(len(result.data), 1)
        self.assertEqual(result.data[0].title, "Test Sound")


    def test_create_or_get_existing_sound_existing(self):
        # IF
        mock_db = Mock()
        sound_data = SoundData(
            title="Test Sound",
            bpm=120,
            duration_in_seconds=180,
            genres=["Pop"],
            credits=[CreditCreate(name="Test Artist", role="VOCALIST")]
        )
        mock_existing_sound = Mock(id=1, title="Test Sound")

        self.mock_sound_repository.get_by_name_and_artist.return_value = mock_existing_sound

        # WHEN
        result = self.service._create_or_get_existing_sound(mock_db, sound_data)

        # THEN
        self.assertEqual(result, mock_existing_sound)


if __name__ == '__main__':
    unittest.main()
