from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.application.sound_service import SoundService
from app.application.playlist_service import PlaylistService
from app.schemas.playlist_schema import PlaylistCreateRequest, PlaylistResponse, PlaylistsResponse
from app.schemas.sound_schema import SoundCreate, SoundsResponse, SoundResponse
from app.api.dependencies import get_db

router = APIRouter()

@router.post("/admin/sounds", response_model=SoundsResponse) #change to soundsresponse
def create_sounds(request_data: SoundCreate, db: Session = Depends(get_db)):
    try:
        return SoundService.create_sounds(db, request_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sounds", response_model=SoundsResponse)
def get_sounds(db: Session = Depends(get_db)):
    try:
        return SoundService.get_sounds(db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/playlists", response_model=PlaylistsResponse)
def create_playlists(request: PlaylistCreateRequest, db: Session = Depends(get_db)):
    try:
        return PlaylistService.create_playlists(db, request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/playlists/by-sound", response_model=PlaylistsResponse)
def get_playlists_by_sound(sound_id: int, db: Session = Depends(get_db)):
    try:
        return PlaylistService.get_playlists_by_sound(db, sound_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sounds/recommended", response_model=SoundsResponse)
def get_recommended_sound(playlistId: int, db: Session = Depends(get_db)):
    try:
        return SoundService.get_recommended_sound(db, playlistId)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))