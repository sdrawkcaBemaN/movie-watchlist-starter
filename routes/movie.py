from flask import Blueprint
from models import Movie

movie_bp = Blueprint("movies", __name__)

# GET /api/movies
@movie_bp.route("/", methods=["GET"])
def get_movies():
    movies = Movie.query.order_by(Movie.id).all()

    return {
        "data": [movie.to_json() for movie in movies]
    }, 200

# GET /api/movies/id
@movie_bp.route("/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        return {"error": "Movie not found"}, 404

    return {
        "data": movie.to_json()
    }, 200
