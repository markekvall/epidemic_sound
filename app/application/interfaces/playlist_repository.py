from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from app.infrastructure.database import Playlist
from typing import List, Optional

class IPlaylistRepository(ABC):
    @abstractmethod
    def create_playlist(self, db: Session, title: str, sound_ids: List[int]) -> Playlist:
        pass

    @abstractmethod
    def get_by_id(self, db: Session, playlist_id: int) -> Optional[Playlist]:
        pass

    @abstractmethod
    def get_by_sound_id(self, db: Session, sound_id: int) -> Optional[Playlist]:
        pass
