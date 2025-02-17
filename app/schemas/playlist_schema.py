from pydantic import BaseModel, ConfigDict
from typing import List

class PlaylistCreate(BaseModel):
    title: str
    sounds: List[int]

class PlaylistCreateRequest(BaseModel):
    data: List[PlaylistCreate]

class PlaylistResponse(BaseModel):
    id: int
    title: str
    sounds: List[int]

    model_config = ConfigDict(from_attributes=True)

class PlaylistsResponse(BaseModel):
    data: List[PlaylistResponse]