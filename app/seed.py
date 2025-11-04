from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .database import Base, engine, SessionLocal
from . import models, crud, schemas

def seed():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    usa = crud.get_or_create_country(db, "United States")
    uk = crud.get_or_create_country(db, "United Kingdom")
    japan = crud.get_or_create_country(db, "Japan")
    south_korea = crud.get_or_create_country(db, "South Korea")
    france = crud.get_or_create_country(db, "France")
    poland = crud.get_or_create_country(db, "Poland")

    # Directors & Publishers
    crud.get_or_create_director(db, "Lana Wachowski & Lilly Wachowski")
    crud.get_or_create_director(db, "Christopher Nolan")
    crud.get_or_create_director(db, "Hayao Miyazaki")
    crud.get_or_create_director(db, "Bong Joon-ho")
    crud.get_or_create_director(db, "Vince Gilligan")
    crud.get_or_create_director(db, "The Duffer Brothers")
    crud.get_or_create_director(db, "Greg Daniels")
    crud.get_or_create_director(db, "David Benioff & D. B. Weiss")
    crud.get_or_create_director(db, "Johan Renck")

    crud.get_or_create_publisher(db, "Nintendo")
    crud.get_or_create_publisher(db, "Sony Interactive Entertainment")
    crud.get_or_create_publisher(db, "Xbox Game Studios")
    crud.get_or_create_publisher(db, "CD PROJEKT RED")
    crud.get_or_create_publisher(db, "Ubisoft")

    # Movies (5)
    movies = [
        ("The Matrix", 1999, "United States", "Lana Wachowski & Lilly Wachowski"),
        ("Inception", 2010, "United States", "Christopher Nolan"),
        ("Spirited Away", 2001, "Japan", "Hayao Miyazaki"),
        ("The Dark Knight", 2008, "United States", "Christopher Nolan"),
        ("Parasite", 2019, "South Korea", "Bong Joon-ho"),
    ]
    for title, year, country, director in movies:
        crud.create_movie(db, schemas.MovieCreate(
            title=title, year=year, country_name=country, director_name=director
        ))

    # Series (5) with seasons/episodes
    series_list = [
        ("Breaking Bad", 2008, "United States", "Vince Gilligan",
         [
             {"number":1, "year":2008, "episodes":[{"number":1,"title":"Pilot"},{"number":2,"title":"Cat's in the Bag..."}]},
             {"number":2, "year":2009, "episodes":[{"number":1,"title":"Seven Thirty-Seven"},{"number":2,"title":"Grilled"}]}
         ]),
        ("Stranger Things", 2016, "United States", "The Duffer Brothers",
         [
             {"number":1, "year":2016, "episodes":[{"number":1,"title":"Chapter One"},{"number":2,"title":"Chapter Two"}]},
             {"number":2, "year":2017, "episodes":[{"number":1,"title":"MADMAX"},{"number":2,"title":"Trick or Treat, Freak"}]}
         ]),
        ("The Office (US)", 2005, "United States", "Greg Daniels",
         [
             {"number":1, "year":2005, "episodes":[{"number":1,"title":"Pilot"},{"number":2,"title":"Diversity Day"}]},
             {"number":2, "year":2005, "episodes":[{"number":1,"title":"The Dundies"},{"number":2,"title":"Sexual Harassment"}]}
         ]),
        ("Game of Thrones", 2011, "United States", "David Benioff & D. B. Weiss",
         [
             {"number":1, "year":2011, "episodes":[{"number":1,"title":"Winter Is Coming"},{"number":2,"title":"The Kingsroad"}]},
             {"number":2, "year":2012, "episodes":[{"number":1,"title":"The North Remembers"},{"number":2,"title":"The Night Lands"}]}
         ]),
        ("Chernobyl", 2019, "United Kingdom", "Johan Renck",
         [
             {"number":1, "year":2019, "episodes":[{"number":1,"title":"1:23:45"},{"number":2,"title":"Please Remain Calm"}]}
         ]),
    ]
    for title, year, country, director, seasons in series_list:
        payload = schemas.SeriesCreate(
            title=title, year=year, country_name=country, director_name=director,
            seasons=[schemas.SeasonCreate(
                number=sc["number"], year=sc.get("year"),
                episodes=[schemas.EpisodeCreate(**ep) for ep in sc.get("episodes", [])]
            ) for sc in seasons]
        )
        crud.create_series(db, payload)

    # Games (5)
    games = [
        ("The Legend of Zelda: Breath of the Wild", 2017, "Japan", "Nintendo"),
        ("The Last of Us Part II", 2020, "United States", "Sony Interactive Entertainment"),
        ("Halo Infinite", 2021, "United States", "Xbox Game Studios"),
        ("The Witcher 3: Wild Hunt", 2015, "Poland", "CD PROJEKT RED"),
        ("Assassin's Creed Valhalla", 2020, "France", "Ubisoft"),
    ]
    for title, year, country, publisher in games:
        crud.create_game(db, schemas.GameCreate(
            title=title, year=year, country_name=country, publisher_name=publisher
        ))

    print("Seed OK: 5 movies, 5 series (with seasons/episodes) and 5 games inserted.")

if __name__ == "__main__":
    try:
        seed()
    except IntegrityError:
        print("Seed: some records already exist, skipping duplicates.")
