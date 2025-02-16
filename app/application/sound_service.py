import logging
import random
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.database import Sound
from app.infrastructure.sound_repo import SoundRepository
from app.schemas.sound_schema import SoundCreate, SoundsResponse, SoundResponse, GenreResponse, CreditResponse
from app.infrastructure.playlist_repo import PlaylistRepository

logger = logging.getLogger(__name__)

class SoundService:

    @staticmethod
    def _create_sound_response(sound: Sound) -> SoundResponse:
        return SoundResponse(
            id=sound.id,
            title=sound.title,
            bpm=sound.bpm,
            duration_in_seconds=sound.duration_in_seconds,
            genres=[GenreResponse.from_orm(genre) for genre in sound.genres],
            credits=[CreditResponse.from_orm(credit) for credit in sound.credits]
        )


    @staticmethod
    def create_sounds(db: Session, request_data: SoundCreate) -> SoundsResponse:
        logger.info("Creating sounds...") #make more detailed
        
        sound_responses = []

        with db.begin():
            try:
                for sound_data in request_data.data:
                    existing_sound = SoundRepository.get_by_name_and_artist(db, sound_data.title, sound_data.credits[0].name)
                    
                    if existing_sound:
                        logger.warning(f"Sound '{sound_data.title}' by '{sound_data.credits[0].name}' already exists. Returning existing song.")
                        sound = existing_sound
                    else:
                        sound = SoundRepository.create(db, sound_data)
                    
                    sound_responses.append(SoundService._create_sound_response(sound))

            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                db.rollback()
                raise

        return SoundsResponse(data=sound_responses)
    

    @staticmethod
    def get_sounds(db: Session):
        logger.info("Fetching all sounds...")

        sounds = SoundRepository.get_all(db)
        sound_responses = [SoundService._create_sound_response(sound) for sound in sounds]
        
        return SoundsResponse(data=sound_responses)


    @staticmethod
    def get_recommended_sound(db: Session, playlist_id: int) -> SoundsResponse:
        
        playlist = PlaylistRepository.get_by_id(db, playlist_id)
        if not playlist:
            raise HTTPException(status_code=404, detail="Playlist not found")
        
        playlist_sounds = playlist.sounds
        playlist_genres = {genre.id for sound in playlist_sounds for genre in sound.genres}

        if not playlist_genres:
            raise HTTPException(status_code=400, detail="Playlist has no genres")

        # Get all sounds, filtering those that share at least one genre with the playlist
        all_sounds = SoundRepository.get_all(db)
        genre_matched_sounds = [
            sound for sound in all_sounds
            if any(genre.id in playlist_genres for genre in sound.genres) and sound.id not in {s.id for s in playlist_sounds}
        ]

        # If we have matching sounds, pick a random one
        if genre_matched_sounds:
            selected_sound = random.choice(genre_matched_sounds)
        else:
            # If no genre-based match is found, return any random sound (excluding playlist sounds)
            available_sounds = [s for s in all_sounds if s.id not in {s.id for s in playlist_sounds}]
            selected_sound = random.choice(available_sounds) if available_sounds else None

        if not selected_sound:
            raise HTTPException(status_code=404, detail="No suitable recommendations found")
            
        recommended_sound = SoundService._create_sound_response(selected_sound)
        
        return SoundsResponse(data=[recommended_sound])