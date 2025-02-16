from typing import List
from sqlalchemy.orm import Session, joinedload
from app.infrastructure.database import Playlist, Sound

class PlaylistRepository:
    @staticmethod
    def create_playlist(db: Session, title: str, sound_ids: List[int]) -> Playlist:
        # Fetch sounds by IDs
        sounds = db.query(Sound).filter(Sound.id.in_(sound_ids)).all()
        
        # Create a new playlist
        playlist = Playlist(title=title, sounds=sounds)
        db.add(playlist)
        db.commit()
        db.refresh(playlist)

        return playlist


    @staticmethod
    def get_by_id(db: Session, playlist_id: int) -> Playlist | None:
        return (
            db.query(Playlist)
            .filter(Playlist.id == playlist_id)
            .options(
                # Eagerly load sounds and their genres
                joinedload(Playlist.sounds).joinedload(Sound.genres)
            )
            .first()
        )


    @staticmethod
    def get_by_sound_id(db: Session, sound_id: int) -> Playlist | None:
        return db.query(Playlist).join(Playlist.sounds).filter(Sound.id == sound_id).all()
