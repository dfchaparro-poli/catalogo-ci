from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from . import models, schemas

def get_or_create_country(db: Session, name: str) -> models.Country:
    name = name.strip()
    obj = db.query(models.Country).filter_by(name=name).first()
    if not obj:
        obj = models.Country(name=name)
        db.add(obj); db.commit(); db.refresh(obj)
    return obj

def get_or_create_director(db: Session, name: str) -> models.Director:
    name = name.strip()
    obj = db.query(models.Director).filter_by(name=name).first()
    if not obj:
        obj = models.Director(name=name)
        db.add(obj); db.commit(); db.refresh(obj)
    return obj

def get_or_create_publisher(db: Session, name: str) -> models.Publisher:
    name = name.strip()
    obj = db.query(models.Publisher).filter_by(name=name).first()
    if not obj:
        obj = models.Publisher(name=name)
        db.add(obj); db.commit(); db.refresh(obj)
    return obj

def list_movies(db: Session, year: Optional[int]=None, country: Optional[str]=None, director: Optional[str]=None) -> List[models.Movie]:
    q = db.query(models.Movie).options(joinedload(models.Movie.country), joinedload(models.Movie.director))
    if year: q = q.filter(models.Movie.year == year)
    if country: q = q.join(models.Country).filter(models.Country.name == country)
    if director: q = q.join(models.Director).filter(models.Director.name == director)
    return q.order_by(models.Movie.year.desc(), models.Movie.title.asc()).all()

def get_movie(db: Session, movie_id: int) -> Optional[models.Movie]:
    return db.query(models.Movie)\
        .options(joinedload(models.Movie.country), joinedload(models.Movie.director))\
        .filter(models.Movie.id == movie_id).first()

def create_movie(db: Session, data: schemas.MovieCreate) -> models.Movie:
    country = get_or_create_country(db, data.country_name)
    director = get_or_create_director(db, data.director_name)
    m = models.Movie(title=data.title, year=data.year, country_id=country.id, director_id=director.id)
    db.add(m); db.commit(); db.refresh(m)
    return get_movie(db, m.id)

def update_movie(db: Session, m: models.Movie, data: schemas.MovieUpdate) -> models.Movie:
    if data.title is not None: m.title = data.title
    if data.year is not None: m.year = data.year
    if data.country_name is not None:
        c = get_or_create_country(db, data.country_name); m.country_id = c.id
    if data.director_name is not None:
        d = get_or_create_director(db, data.director_name); m.director_id = d.id
    db.add(m); db.commit(); db.refresh(m)
    return get_movie(db, m.id)

def delete_movie(db: Session, m: models.Movie) -> None:
    db.delete(m); db.commit()

def list_series(db: Session, year: Optional[int]=None, country: Optional[str]=None, director: Optional[str]=None) -> List[models.Series]:
    q = db.query(models.Series).options(
        joinedload(models.Series.country),
        joinedload(models.Series.director),
        joinedload(models.Series.seasons).joinedload(models.Season.episodes)
    )
    if year: q = q.filter(models.Series.year == year)
    if country: q = q.join(models.Country).filter(models.Country.name == country)
    if director: q = q.join(models.Director).filter(models.Director.name == director)
    return q.order_by(models.Series.year.desc(), models.Series.title.asc()).all()

def get_series(db: Session, series_id: int) -> Optional[models.Series]:
    return db.query(models.Series)\
        .options(
            joinedload(models.Series.country),
            joinedload(models.Series.director),
            joinedload(models.Series.seasons).joinedload(models.Season.episodes)
        ).filter(models.Series.id == series_id).first()

def create_series(db: Session, data: schemas.SeriesCreate) -> models.Series:
    country = get_or_create_country(db, data.country_name)
    director = get_or_create_director(db, data.director_name)
    s = models.Series(title=data.title, year=data.year, country_id=country.id, director_id=director.id)
    db.add(s); db.commit(); db.refresh(s)
    for sc in data.seasons:
        season = models.Season(series_id=s.id, number=sc.number, year=sc.year)
        db.add(season); db.commit(); db.refresh(season)
        for ec in sc.episodes:
            ep = models.Episode(season_id=season.id, number=ec.number, title=ec.title)
            db.add(ep)
        db.commit()
    return get_series(db, s.id)

def update_series(db: Session, s: models.Series, data: schemas.SeriesUpdate) -> models.Series:
    if data.title is not None: s.title = data.title
    if data.year is not None: s.year = data.year
    if data.country_name is not None:
        c = get_or_create_country(db, data.country_name); s.country_id = c.id
    if data.director_name is not None:
        d = get_or_create_director(db, data.director_name); s.director_id = d.id
    db.add(s); db.commit(); db.refresh(s)
    return get_series(db, s.id)

def delete_series(db: Session, s: models.Series) -> None:
    db.delete(s); db.commit()

def add_season(db: Session, series_id: int, season_data: schemas.SeasonCreate) -> models.Series:
    season = models.Season(series_id=series_id, number=season_data.number, year=season_data.year)
    db.add(season); db.commit(); db.refresh(season)
    for ec in season_data.episodes:
        ep = models.Episode(season_id=season.id, number=ec.number, title=ec.title)
        db.add(ep)
    db.commit()
    return get_series(db, series_id)

def list_games(db: Session, year: Optional[int]=None, country: Optional[str]=None, publisher: Optional[str]=None) -> List[models.Game]:
    q = db.query(models.Game).options(joinedload(models.Game.country), joinedload(models.Game.publisher))
    if year: q = q.filter(models.Game.year == year)
    if country: q = q.join(models.Country).filter(models.Country.name == country)
    if publisher: q = q.join(models.Publisher).filter(models.Publisher.name == publisher)
    return q.order_by(models.Game.year.desc(), models.Game.title.asc()).all()

def get_game(db: Session, game_id: int) -> Optional[models.Game]:
    return db.query(models.Game)\
        .options(joinedload(models.Game.country), joinedload(models.Game.publisher))\
        .filter(models.Game.id == game_id).first()

def create_game(db: Session, data: schemas.GameCreate) -> models.Game:
    country = get_or_create_country(db, data.country_name)
    publisher = get_or_create_publisher(db, data.publisher_name)
    g = models.Game(title=data.title, year=data.year, country_id=country.id, publisher_id=publisher.id)
    db.add(g); db.commit(); db.refresh(g)
    return get_game(db, g.id)

def update_game(db: Session, g: models.Game, data: schemas.GameUpdate) -> models.Game:
    if data.title is not None: g.title = data.title
    if data.year is not None: g.year = data.year
    if data.country_name is not None:
        c = get_or_create_country(db, data.country_name); g.country_id = c.id
    if data.publisher_name is not None:
        p = get_or_create_publisher(db, data.publisher_name); g.publisher_id = p.id
    db.add(g); db.commit(); db.refresh(g)
    return get_game(db, g.id)

def delete_game(db: Session, g: models.Game) -> None:
    db.delete(g); db.commit()

def list_countries(db: Session) -> List[models.Country]:
    return db.query(models.Country).order_by(models.Country.name.asc()).all()

def list_directors(db: Session) -> List[models.Director]:
    return db.query(models.Director).order_by(models.Director.name.asc()).all()

def list_publishers(db: Session) -> List[models.Publisher]:
    return db.query(models.Publisher).order_by(models.Publisher.name.asc()).all()
