from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.playlist_schema import PlaylistCreate, PlaylistResponse, PlaylistsResponse
from app.application.interfaces.playlist_repository import IPlaylistRepository

class PlaylistService:

    def __init__(self, repository: IPlaylistRepository):
        self.repository = repository


    def create_playlists(self, db: Session, playlists_data: PlaylistCreate) -> PlaylistsResponse:
        
        created_playlists = []

        for playlist_data in playlists_data.data:

            playlist = self.repository.create_playlist(db, playlist_data.title, playlist_data.sounds)
            created_playlists.append(
                PlaylistResponse(
                    id=playlist.id,
                    title=playlist.title,
                    sounds=[sound.id for sound in playlist.sounds]
                )
            )

        return PlaylistsResponse(data=created_playlists)


    def get_playlists_by_sound(self, db: Session, sound_id: int) -> PlaylistsResponse:

        playlists = self.repository.get_by_sound_id(db, sound_id)

        if not playlists:
            raise HTTPException(status_code=404, detail="No playlists found for this sound")

        playlist_responses = [
            PlaylistResponse(
                id=playlist.id,
                title=playlist.title,
                sounds=[sound.id for sound in playlist.sounds]
            )
            for playlist in playlists
        ]

        return PlaylistsResponse(data=playlist_responses)
