import json
import os
from flask import Blueprint, request
from models import Movie
from google import genai
from dotenv import load_dotenv

load_dotenv()
movie_bp = Blueprint("movies", __name__)

# GET /api/movies
@movie_bp.route("/", methods=["GET"], strict_slashes=False)
def get_movies():

    query = Movie.query
    genre = request.args.get("genre")
    search = request.args.get("search")

    if genre:
        query = query.filter(Movie.genres.like(f'%{genre}%'))
    if search:
        query = query.filter(Movie.title.like(f"%{search}%"))

    movies = query.order_by(Movie.id).all()

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

# POST /api/movies/recommend    
@movie_bp.route("/recommend", methods=["POST"])
def recommend_movies():
    data = request.get_json() or {}
    prompt = data.get("prompt")
    if not prompt:
        return {"error": "Prompt is required"}, 400

    movies = Movie.query.all()
    if not movies:
        return {"error": "No movies available"}, 404

    movie_list = []
    for movie in movies:
        movie_list.append({
            "id": movie.id,
            "title": movie.title,
            "year": movie.year,
            "genres": movie.genres,
            "synopsis": movie.synopsis
        })

    api_key = os.getenv("API_KEY")
    if not api_key:
        return {"error": "Gemini API key is missing"}, 500

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents="You are a movie recommendation giver."
          "From the following list of movies and the users prompt, you need to recommend a movie that best fits the users request. "
          "Only select the movies from the list below and do not recommend any other movies. "
          "Give only the movie ID and a give a reasoning for your choice.\n\nMovies:\n" + json.dumps(movie_list) + "\n\nUser Prompt: " + prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    result = json.loads(response.text)

    selected_movie = Movie.query.get(result.get("movie_id"))

    if not selected_movie:
        return {"error": "Gemini returned an invalid movie ID"}, 500

    return {
        "movie_id": selected_movie.id,
        "reasoning": result.get("reasoning")
    }, 200
