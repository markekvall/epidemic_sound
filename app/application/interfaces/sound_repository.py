from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from app.infrastructure.database import Sound, Genre
from typing import List

class ISoundRepository(ABC):
    @abstractmethod
    def create_sound(self, db: Session, sound_data) -> Sound:
        pass

    @abstractmethod
    def get_by_name_and_artist(self, db: Session, title: str, artist_name: str) -> Sound:
        pass

    @abstractmethod
    def get_all(self, db: Session) -> Sound | None:
        pass

    @abstractmethod
    def get_all_from_genre_not_in_playlist(self, db: Session, playlist_sounds: list[Sound], playlist_genre_ids: set[int]) -> list[Sound] | None:
        pass