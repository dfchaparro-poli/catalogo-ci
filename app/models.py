from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base

class Country(Base):
    __tablename__ = "countries"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, index=True, nullable=False)

class Director(Base):
    __tablename__ = "directors"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True, index=True, nullable=False)

class Publisher(Base):
    __tablename__ = "publishers"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True, index=True, nullable=False)

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    title = Column(String(150), index=True, nullable=False)
    year = Column(Integer, nullable=False)
    director_id = Column(Integer, ForeignKey("directors.id"), nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    director = relationship("Director")
    country = relationship("Country")
    __table_args__ = (UniqueConstraint("title", "year", name="uq_movies_title_year"),)

class Series(Base):
    __tablename__ = "series"
    id = Column(Integer, primary_key=True)
    title = Column(String(150), index=True, nullable=False)
    year = Column(Integer, nullable=False)
    director_id = Column(Integer, ForeignKey("directors.id"), nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    director = relationship("Director")
    country = relationship("Country")
    seasons = relationship("Season", back_populates="series", cascade="all, delete-orphan")
    __table_args__ = (UniqueConstraint("title", "year", name="uq_series_title_year"),)

class Season(Base):
    __tablename__ = "seasons"
    id = Column(Integer, primary_key=True)
    series_id = Column(Integer, ForeignKey("series.id"), nullable=False)
    number = Column(Integer, nullable=False)
    year = Column(Integer, nullable=True)
    series = relationship("Series", back_populates="seasons")
    episodes = relationship("Episode", back_populates="season", cascade="all, delete-orphan")
    __table_args__ = (UniqueConstraint("series_id", "number", name="uq_season_series_number"),)

class Episode(Base):
    __tablename__ = "episodes"
    id = Column(Integer, primary_key=True)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)
    number = Column(Integer, nullable=False)
    title = Column(String(150), nullable=False)
    season = relationship("Season", back_populates="episodes")
    __table_args__ = (UniqueConstraint("season_id", "number", name="uq_episode_season_number"),)

class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True)
    title = Column(String(150), index=True, nullable=False)
    year = Column(Integer, nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    publisher_id = Column(Integer, ForeignKey("publishers.id"), nullable=False)
    country = relationship("Country")
    publisher = relationship("Publisher")
    __table_args__ = (UniqueConstraint("title", "year", name="uq_games_title_year"),)
