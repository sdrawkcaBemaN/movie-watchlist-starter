import json
from pathlib import Path

from app import app
from db import db
from models import Movie


BASE_DIR = Path(__file__).resolve().parent
MOVIES_FILE = BASE_DIR / "data" / "movies.json"


def seed_movies():
    with open(MOVIES_FILE, "r", encoding="utf-8") as file:
        movies_data = json.load(file)

    added = 0
    skipped = 0

    for movie_data in movies_data:

        existing_movie = db.session.get(Movie, movie_data["id"])

        if existing_movie:
            skipped += 1
            continue

        movie = Movie(**movie_data)

        db.session.add(movie)
        added += 1

    db.session.commit()

    print(f"Seeding completed!")
    print(f"Movies added: {added}")
    print(f"Movies skipped: {skipped}")
    print(f"Total movies in database: {Movie.query.count()}")


if __name__ == "__main__":
    with app.app_context():
        seed_movies()
