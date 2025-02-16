from pydantic import BaseModel
from typing import List

class CreditCreate(BaseModel):
    name: str
    role: str

class SoundData(BaseModel):
    title: str
    bpm: int
    genres: List[str]
    duration_in_seconds: int
    credits: List[CreditCreate]

class SoundCreate(BaseModel):
    data: List[SoundData]

class GenreResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
        from_attributes = True

class CreditResponse(BaseModel):
    id: int
    name: str
    role: str

    class Config:
        orm_mode = True
        from_attributes = True

class SoundResponse(BaseModel):
    id: int
    title: str
    bpm: int
    duration_in_seconds: int
    genres: List[GenreResponse]
    credits: List[CreditResponse]

    class Config:
        orm_mode = True
        from_attributes = True

class SoundsResponse(BaseModel):
    data: List[SoundResponse]