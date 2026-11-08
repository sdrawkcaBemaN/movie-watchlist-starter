from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Watched, Movie, Review
from db import db

watched_bp = Blueprint("watched", __name__)


# GET /api/watched
@watched_bp.route("/", methods=["GET"])
@jwt_required()
def get_watched():
    user_id = int(get_jwt_identity())
    watched_movies = Watched.query.filter_by(user_id=user_id).all()

    result = []

    for item in watched_movies:
        review = Review.query.filter_by(
            user_id=user_id,
            movie_id=item.movie_id
        ).first()

        result.append({
            "id": item.id,
            "movie": item.movie.to_json(),
            "rating": review.rating if review else None,
            "review": review.review if review else None,
            "watched_at": item.watched_at.isoformat()
            if item.watched_at else None
        })

    return {"data": result}, 200


# POST /api/watched
@watched_bp.route("/", methods=["POST"])
@jwt_required()
def add_watched():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    movie_id = data.get("movieId")
    rating =  data.get("rating")
    review_text = data.get("review")

    if not movie_id:
        return {"error": "Movie ID is required"}, 400

    movie = db.session.get(Movie, movie_id)

    if not movie:
        return {"error": "Movie not found"}, 404

    existing = Watched.query.filter_by(
        user_id=user_id,
        movie_id=movie_id
    ).first()

    if existing:
        return {"error": "Movie already marked as watched"}, 409

    new_watched = Watched(
        user_id=user_id,
        movie_id=movie_id
    )
    new_review = Review(
        user_id=user_id,
        movie_id=movie_id,
        rating=rating,
        review=review_text
    )
    db.session.add(new_watched)
    db.session.add(new_review)
    db.session.commit()

    return {
        "message": "Movie marked as watched",
        "data": new_watched.to_json()
    }, 201