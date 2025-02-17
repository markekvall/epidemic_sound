from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.infrastructure.database import Playlist, Sound
from app.application.interfaces.playlist_repository import IPlaylistRepository

class PlaylistRepository(IPlaylistRepository):
    def create_playlist(self, db: Session, title: str, sound_ids: List[int]) -> Playlist:
        sounds = db.query(Sound).filter(Sound.id.in_(sound_ids)).all()
        
        playlist = Playlist(title=title, sounds=sounds)
        db.add(playlist)
        db.commit()
        db.refresh(playlist)

        return playlist

    def get_by_id(self, db: Session, playlist_id: int) -> Optional[Playlist]:
        return (
            db.query(Playlist)
            .filter(Playlist.id == playlist_id)
            .options(
                joinedload(Playlist.sounds).joinedload(Sound.genres)
            )
            .first()
        )

    def get_by_sound_id(self, db: Session, sound_id: int) -> Optional[Playlist]:
        return db.query(Playlist).join(Playlist.sounds).filter(Sound.id == sound_id).all()
