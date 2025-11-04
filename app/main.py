from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from .database import Base, engine, SessionLocal
from . import schemas, crud

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Catalog API",
    description="Movies, Series (with seasons/episodes) and Games catalog",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}

@app.get("/countries", response_model=List[schemas.CountryOut], tags=["meta"])
def get_countries(db: Session = Depends(get_db)):
    return crud.list_countries(db)

@app.get("/directors", response_model=List[schemas.DirectorOut], tags=["meta"])
def get_directors(db: Session = Depends(get_db)):
    return crud.list_directors(db)

@app.get("/publishers", response_model=List[schemas.PublisherOut], tags=["meta"])
def get_publishers(db: Session = Depends(get_db)):
    return crud.list_publishers(db)

@app.get("/movies", response_model=List[schemas.MovieOut], tags=["movies"])
def get_movies(year: Optional[int] = Query(None, ge=1888, le=2100), country: Optional[str] = None, director: Optional[str] = None, db: Session = Depends(get_db)):
    return crud.list_movies(db, year=year, country=country, director=director)

@app.get("/movies/{movie_id}", response_model=schemas.MovieOut, tags=["movies"])
def get_movie_by_id(movie_id: int, db: Session = Depends(get_db)):
    m = crud.get_movie(db, movie_id)
    if not m: raise HTTPException(status_code=404, detail="Movie not found")
    return m

@app.post("/movies", response_model=schemas.MovieOut, status_code=201, tags=["movies"])
def create_movie(item: schemas.MovieCreate, db: Session = Depends(get_db)):
    return crud.create_movie(db, item)

@app.put("/movies/{movie_id}", response_model=schemas.MovieOut, tags=["movies"])
def update_movie(movie_id: int, item: schemas.MovieUpdate, db: Session = Depends(get_db)):
    m = crud.get_movie(db, movie_id)
    if not m: raise HTTPException(status_code=404, detail="Movie not found")
    return crud.update_movie(db, m, item)

@app.delete("/movies/{movie_id}", status_code=204, tags=["movies"])
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    m = crud.get_movie(db, movie_id)
    if not m: raise HTTPException(status_code=404, detail="Movie not found")
    crud.delete_movie(db, m); return None

@app.get("/series", response_model=List[schemas.SeriesOut], tags=["series"])
def get_series_list(year: Optional[int] = Query(None, ge=1888, le=2100), country: Optional[str] = None, director: Optional[str] = None, db: Session = Depends(get_db)):
    return crud.list_series(db, year=year, country=country, director=director)

@app.get("/series/{series_id}", response_model=schemas.SeriesOut, tags=["series"])
def get_series_by_id(series_id: int, db: Session = Depends(get_db)):
    s = crud.get_series(db, series_id)
    if not s: raise HTTPException(status_code=404, detail="Series not found")
    return s

@app.post("/series", response_model=schemas.SeriesOut, status_code=201, tags=["series"])
def create_series(item: schemas.SeriesCreate, db: Session = Depends(get_db)):
    return crud.create_series(db, item)

@app.put("/series/{series_id}", response_model=schemas.SeriesOut, tags=["series"])
def update_series(series_id: int, item: schemas.SeriesUpdate, db: Session = Depends(get_db)):
    s = crud.get_series(db, series_id)
    if not s: raise HTTPException(status_code=404, detail="Series not found")
    return crud.update_series(db, s, item)

@app.delete("/series/{series_id}", status_code=204, tags=["series"])
def delete_series(series_id: int, db: Session = Depends(get_db)):
    s = crud.get_series(db, series_id)
    if not s: raise HTTPException(status_code=404, detail="Series not found")
    crud.delete_series(db, s); return None

@app.post("/series/{series_id}/seasons", response_model=schemas.SeriesOut, status_code=201, tags=["series"])
def add_season(series_id: int, season: schemas.SeasonCreate, db: Session = Depends(get_db)):
    if not crud.get_series(db, series_id):
        raise HTTPException(status_code=404, detail="Series not found")
    return crud.add_season(db, series_id, season)

@app.get("/games", response_model=List[schemas.GameOut], tags=["games"])
def get_games(year: Optional[int] = Query(None, ge=1950, le=2100), country: Optional[str] = None, publisher: Optional[str] = None, db: Session = Depends(get_db)):
    return crud.list_games(db, year=year, country=country, publisher=publisher)

@app.get("/games/{game_id}", response_model=schemas.GameOut, tags=["games"])
def get_game_by_id(game_id: int, db: Session = Depends(get_db)):
    g = crud.get_game(db, game_id)
    if not g: raise HTTPException(status_code=404, detail="Game not found")
    return g

@app.post("/games", response_model=schemas.GameOut, status_code=201, tags=["games"])
def create_game(item: schemas.GameCreate, db: Session = Depends(get_db)):
    return crud.create_game(db, item)

@app.put("/games/{game_id}", response_model=schemas.GameOut, tags=["games"])
def update_game(game_id: int, item: schemas.GameUpdate, db: Session = Depends(get_db)):
    g = crud.get_game(db, game_id)
    if not g: raise HTTPException(status_code=404, detail="Game not found")
    return crud.update_game(db, g, item)

@app.delete("/games/{game_id}", status_code=204, tags=["games"])
def delete_game(game_id: int, db: Session = Depends(get_db)):
    g = crud.get_game(db, game_id)
    if not g: raise HTTPException(status_code=404, detail="Game not found")
    crud.delete_game(db, g); return None
