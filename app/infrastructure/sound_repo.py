from sqlalchemy.orm import Session, joinedload
from app.infrastructure.database import Sound, Credit, Genre

class SoundRepository:
    @staticmethod
    def create(db: Session, sound_data) -> Sound:
        
        sound = Sound(
            title=sound_data.title,
            bpm=sound_data.bpm,
            duration_in_seconds=sound_data.duration_in_seconds
        )

        genres = []
        for genre_name in sound_data.genres:
            genre = db.query(Genre).filter(Genre.name == genre_name).first()
            if not genre:
                genre = Genre(name=genre_name)
                genres.append(genre)
            sound.genres.append(genre)
        
        if genres:
            db.bulk_save_objects(genres)

        db.add(sound)
        db.flush()

        credits = [Credit(name=credit_data.name, role=credit_data.role, sound_id=sound.id) 
                   for credit_data in sound_data.credits]
        db.bulk_save_objects(credits)

        db.flush()
        db.refresh(sound)
        return sound
        

    @staticmethod
    def get_by_name_and_artist(db: Session, title: str, artist_name: str) -> Sound:
        return db.query(Sound).join(Credit).filter(
            Sound.title == title,
            Credit.name == artist_name
        ).first()


    @staticmethod
    def get_all(db: Session):
        sounds = db.query(Sound).options(
            joinedload(Sound.credits), 
            joinedload(Sound.genres)
        ).all()

        return sounds