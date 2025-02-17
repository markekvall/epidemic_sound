import logging
import random
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.infrastructure.database import Sound
from app.schemas.sound_schema import SoundCreate, SoundData, SoundsResponse, SoundResponse, GenreResponse, CreditResponse
from app.application.interfaces.sound_repository import ISoundRepository
from app.application.interfaces.playlist_repository import IPlaylistRepository


logger = logging.getLogger(__name__)

class SoundService:

    def __init__(self, sound_repository: ISoundRepository, playlist_repo: IPlaylistRepository):
        self.sound_repository = sound_repository
        self.playlist_repo = playlist_repo

    @staticmethod
    def _create_sound_response(sound: Sound) -> SoundResponse:
        return SoundResponse(
            id=sound.id,
            title=sound.title,
            bpm=sound.bpm,
            duration_in_seconds=sound.duration_in_seconds,
            genres=[GenreResponse.model_validate(genre) for genre in sound.genres],
            credits=[CreditResponse.model_validate(credit) for credit in sound.credits]
        )


    def create_sounds(self, db: Session, request_data: SoundCreate) -> SoundsResponse:
        logger.info(f"Attempting to create {len(request_data.data)} sounds...")      

        sound_responses = []

        for sound_data in request_data.data:
            try:
                sound = self._create_or_get_existing_sound(db, sound_data)
                sound_responses.append(self._create_sound_response(sound))
            except SQLAlchemyError as e:
                logger.error(f"Error creating sound '{sound_data.title}': {str(e)}")
                continue

        logger.info(f"Successfully processed {len(sound_responses)} out of {len(request_data.data)} sounds.")
        return SoundsResponse(data=sound_responses)
    

    def get_sounds(self, db: Session):
        logger.info("Fetching all sounds...")

        sounds = self.sound_repository.get_all(db)
        sound_responses = [SoundService._create_sound_response(sound) for sound in sounds]
        
        return SoundsResponse(data=sound_responses)


    def get_recommended_sound(self, db: Session, playlist_id: int) -> SoundsResponse:
        logger.info("Fetching recommended sound...")

        playlist = self.playlist_repo.get_by_id(db, playlist_id)
        if not playlist:
            raise HTTPException(status_code=404, detail="Playlist not found")
        
        playlist_sounds = playlist.sounds
        playlist_genre_ids = {genre.id for sound in playlist_sounds for genre in sound.genres}

        if not playlist_genre_ids:
            raise HTTPException(status_code=400, detail="Playlist has no genres")

        genre_matched_sounds = self.sound_repository.get_all_from_genre_not_in_playlist(db, playlist_sounds, playlist_genre_ids)

        if genre_matched_sounds:
            selected_sound = random.choice(genre_matched_sounds)
        else:
            logger.info("No genre match found, getting random sound")
            available_sounds = self.sound_repository.get_all(db)
            selected_sound = random.choice(available_sounds) if available_sounds else None

        if not selected_sound:
            raise HTTPException(status_code=404, detail="No suitable recommendations found")
            
        recommended_sound = SoundService._create_sound_response(selected_sound)
        
        return SoundsResponse(data=[recommended_sound])
    

    def _create_or_get_existing_sound(self, db: Session, sound_data: SoundData) -> Sound:
        artist_name = sound_data.credits[0].name
        existing_sound = self.sound_repository.get_by_name_and_artist(db, sound_data.title, artist_name)
        
        if existing_sound:
            logger.warning(f"Sound '{sound_data.title}' by '{artist_name}' already exists. Returning existing song.")
            return existing_sound
        
        return self.sound_repository.create_sound(db, sound_data)