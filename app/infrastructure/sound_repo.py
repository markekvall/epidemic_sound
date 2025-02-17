from typing import List, Optional, Set
from sqlalchemy.orm import Session, joinedload
from app.infrastructure.database import Sound, Credit, Genre, sound_credit
from app.application.interfaces.sound_repository import ISoundRepository

class SoundRepository(ISoundRepository):

    def create_sound(self, db: Session, sound_data) -> Sound:
        try:
            sound = Sound(
                title=sound_data.title,
                bpm=sound_data.bpm,
                duration_in_seconds=sound_data.duration_in_seconds
            )

            for genre_name in sound_data.genres:
                genre = db.query(Genre).filter(
                    Genre.name == genre_name).first()
                
                if genre is None:
                    genre = Genre(name=genre_name)
                    db.add(genre)
                    db.flush()
                sound.genres.append(genre)

            db.add(sound)

            for credit_data in sound_data.credits:
                credit = db.query(Credit).filter(
                    Credit.name == credit_data.name,
                    Credit.role == credit_data.role
                ).first()

                if credit is None:
                    credit = Credit(name=credit_data.name, role=credit_data.role)
                    db.add(credit)
                    db.flush()
                sound.credits.append(credit)

            db.commit()
            db.refresh(sound)
            return sound
        
        except Exception as e:
            db.rollback()
            raise e
        

    def get_by_name_and_artist(self, db: Session, title: str, artist_name: str) -> Optional[Sound]:
        return db.query(Sound).join(
            sound_credit).join(Credit).filter(
            Sound.title == title,
            Credit.name == artist_name
        ).first()


    def get_all(self, db: Session) -> Optional[List[Sound]]:
        return db.query(Sound).options(
            joinedload(Sound.credits), 
            joinedload(Sound.genres)
        ).all()

    
    def get_all_from_genre_not_in_playlist(self, db: Session, playlist_sounds: List[Sound], playlist_genre_ids: Set[int]) -> Optional[List[Sound]]:
        playlist_sound_ids = {sound.id for sound in playlist_sounds}

        sounds = db.query(Sound).join(Sound.genres).filter(
            Genre.id.in_(playlist_genre_ids),
            Sound.id.notin_(playlist_sound_ids)
        ).all()

        return sounds
            