from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./sound_library.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

sound_genre = Table('sound_genre', Base.metadata,
    Column('sound_id', Integer, ForeignKey('sounds.id')),
    Column('genre_id', Integer, ForeignKey('genres.id'))
)

playlist_sound = Table(
    "playlist_sound",
    Base.metadata,
    Column("playlist_id", Integer, ForeignKey("playlists.id")),
    Column("sound_id", Integer, ForeignKey("sounds.id"))
)

class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)

    # Many-to-many relationship with Sound
    sounds = relationship("Sound", secondary=playlist_sound, back_populates="playlists")


class Sound(Base):
    __tablename__ = "sounds"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    bpm = Column(Integer, nullable=False)
    duration_in_seconds = Column(Integer, nullable=False)

    credits = relationship("Credit", back_populates="sound", cascade="all, delete-orphan")
    genres = relationship("Genre", secondary=sound_genre, back_populates="sounds")
    playlists = relationship("Playlist", secondary=playlist_sound, back_populates="sounds")


class Credit(Base):
    __tablename__ = "credits"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    sound_id = Column(Integer, ForeignKey("sounds.id"), nullable=False)

    sound = relationship("Sound", back_populates="credits")

class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    sounds = relationship("Sound", secondary=sound_genre, back_populates="genres")

def init_db():
    Base.metadata.create_all(bind=engine)