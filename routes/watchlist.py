from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Watchlist, Movie
from db import db

watchlist_bp = Blueprint("watchlist", __name__)

# GET /api/watchlist
@watchlist_bp.route("/", methods=["GET"])
@jwt_required()
def get_watchlist():
    user_id = int(get_jwt_identity())
    watchlist = Watchlist.query.filter_by(user_id=user_id).all()

    return {
        "data": [item.to_json() for item in watchlist]
    }, 200

# POST /api/watchlist
@watchlist_bp.route("/", methods=["POST"])
@jwt_required()
def add_to_watchlist():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    movie_id = data.get("movie_id")

    if not movie_id:
        return {"error": "Movie ID is required"}, 400

    movie = Movie.query.get(movie_id)

    if not movie:
        return {"error": "Movie not found"}, 404

    existing = Watchlist.query.filter_by(
        user_id=user_id,
        movie_id=movie_id
    ).first()

    if existing:
        return {"error": "Movie already in watchlist"}, 409

    new_item = Watchlist(
        user_id=user_id,
        movie_id=movie_id
    )
    db.session.add(new_item)
    db.session.commit()

    return {
        "message": "Movie added to watchlist",
        "data": new_item.to_json()
    }, 201

# DELETE /api/watchlist/<watchlist_id>
@watchlist_bp.route("/<int:watchlist_id>", methods=["DELETE"])
@jwt_required()
def remove_from_watchlist(watchlist_id):
    user_id = int(get_jwt_identity())
    item = Watchlist.query.filter_by(
        id=watchlist_id,
        user_id=user_id
    ).first()

    if not item:
        return {"error": "Watchlist item not found"}, 404
    db.session.delete(item)
    db.session.commit()

    return {"message": "Movie removed from watchlist"}, 200