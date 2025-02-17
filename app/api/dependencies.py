from app.infrastructure.database import SessionLocal
from fastapi import Depends
from app.infrastructure.sound_repo import SoundRepository
from app.infrastructure.playlist_repo import PlaylistRepository
from app.application.sound_service import SoundService
from app.application.playlist_service import PlaylistService

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_sound_repository():
    return SoundRepository()

def get_playlist_repository():
    return PlaylistRepository()

def get_sound_service(
    sound_repo: SoundRepository = Depends(get_sound_repository),
    playlist_repo: PlaylistRepository = Depends(get_playlist_repository)
):
    return SoundService(sound_repo, playlist_repo)

def get_playlist_service(playlist_repo: PlaylistRepository = Depends(get_playlist_repository)):
    return PlaylistService(playlist_repo)