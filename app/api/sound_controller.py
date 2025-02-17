from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.application.sound_service import SoundService
from app.application.playlist_service import PlaylistService
from app.schemas.playlist_schema import PlaylistCreateRequest, PlaylistResponse, PlaylistsResponse
from app.schemas.sound_schema import SoundCreate, SoundsResponse, SoundResponse
from app.infrastructure.playlist_repo import PlaylistRepository
from app.infrastructure.sound_repo import SoundRepository
from app.api.dependencies import get_db, get_sound_service, get_playlist_service

router = APIRouter()

@router.post("/admin/sounds", response_model=SoundsResponse)
def create_sounds(request_data: SoundCreate, db: Session = Depends(get_db), sound_service: SoundService = Depends(get_sound_service)):
    try:
        return sound_service.create_sounds(db, request_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sounds", response_model=SoundsResponse)
def get_sounds(db: Session = Depends(get_db), sound_service: SoundService = Depends(get_sound_service)):
    try:
        return sound_service.get_sounds(db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/playlists", response_model=PlaylistsResponse)
def create_playlists(request: PlaylistCreateRequest, db: Session = Depends(get_db), playlist_service: PlaylistService = Depends(get_playlist_service)):
    try:
        return playlist_service.create_playlists(db, request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/playlists/by-sound", response_model=PlaylistsResponse)
def get_playlists_by_sound(sound_id: int, db: Session = Depends(get_db), playlist_service: PlaylistService = Depends(get_playlist_service)):
    try:
        return playlist_service.get_playlists_by_sound(db, sound_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sounds/recommended", response_model=SoundsResponse)
def get_recommended_sound(playlistId: int, db: Session = Depends(get_db), sound_service: SoundService = Depends(get_sound_service)):
    try:
        return sound_service.get_recommended_sound(db, playlistId)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))