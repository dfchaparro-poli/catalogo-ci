from typing import List, Optional
from pydantic import BaseModel, Field

class CountryOut(BaseModel):
    id: int
    name: str
    class Config: from_attributes = True

class DirectorOut(BaseModel):
    id: int
    name: str
    class Config: from_attributes = True

class PublisherOut(BaseModel):
    id: int
    name: str
    class Config: from_attributes = True

class MovieBase(BaseModel):
    title: str
    year: int = Field(..., ge=1888, le=2100)
    director_name: str
    country_name: str

class MovieCreate(MovieBase): pass

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    year: Optional[int] = Field(None, ge=1888, le=2100)
    director_name: Optional[str] = None
    country_name: Optional[str] = None

class MovieOut(BaseModel):
    id: int
    title: str
    year: int
    director: DirectorOut
    country: CountryOut
    class Config: from_attributes = True

class EpisodeBase(BaseModel):
    number: int = Field(..., ge=1)
    title: str

class EpisodeCreate(EpisodeBase): pass

class EpisodeOut(BaseModel):
    id: int
    number: int
    title: str
    class Config: from_attributes = True

class SeasonBase(BaseModel):
    number: int = Field(..., ge=1)
    year: Optional[int] = Field(None, ge=1888, le=2100)

class SeasonCreate(SeasonBase):
    episodes: List[EpisodeCreate] = []

class SeasonOut(BaseModel):
    id: int
    number: int
    year: Optional[int]
    episodes: List[EpisodeOut] = []
    class Config: from_attributes = True

class SeriesBase(BaseModel):
    title: str
    year: int = Field(..., ge=1888, le=2100)
    director_name: str
    country_name: str

class SeriesCreate(SeriesBase):
    seasons: List[SeasonCreate] = []

class SeriesUpdate(BaseModel):
    title: Optional[str] = None
    year: Optional[int] = Field(None, ge=1888, le=2100)
    director_name: Optional[str] = None
    country_name: Optional[str] = None

class SeriesOut(BaseModel):
    id: int
    title: str
    year: int
    director: DirectorOut
    country: CountryOut
    seasons: List[SeasonOut] = []
    class Config: from_attributes = True

class GameBase(BaseModel):
    title: str
    year: int = Field(..., ge=1950, le=2100)
    country_name: str
    publisher_name: str

class GameCreate(GameBase): pass

class GameUpdate(BaseModel):
    title: Optional[str] = None
    year: Optional[int] = Field(None, ge=1950, le=2100)
    country_name: Optional[str] = None
    publisher_name: Optional[str] = None

class GameOut(BaseModel):
    id: int
    title: str
    year: int
    country: CountryOut
    publisher: PublisherOut
    class Config: from_attributes = True
