from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from app.infrastructure.database import Sound
from typing import List, Optional, Set

class ISoundRepository(ABC):
    @abstractmethod
    def create_sound(self, db: Session, sound_data) -> Sound:
        pass

    @abstractmethod
    def get_by_name_and_artist(self, db: Session, title: str, artist_name: str) -> Sound:
        pass

    @abstractmethod
    def get_all(self, db: Session) -> Optional[Sound]:
        pass

    @abstractmethod
    def get_all_from_genre_not_in_playlist(self, db: Session, playlist_sounds: List[Sound], playlist_genre_ids: Set[int]) -> List[Sound] | None:
        pass