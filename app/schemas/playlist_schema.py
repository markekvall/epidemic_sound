from pydantic import BaseModel
from typing import List

class PlaylistCreate(BaseModel):
    title: str
    sounds: List[int]  # Accepting sound IDs as strings

class PlaylistCreateRequest(BaseModel):
    data: List[PlaylistCreate]

class PlaylistResponse(BaseModel):
    id: int
    title: str
    sounds: List[int]  # Returning only sound IDs

    class Config:
        orm_mode = True #change to "from_attributes"
        from_attributes = True

class PlaylistsResponse(BaseModel):
    data: List[PlaylistResponse]