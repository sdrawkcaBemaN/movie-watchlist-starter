import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from db import db
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__, instance_path='/tmp/instance')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/watchlist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-fallback-key')

db.init_app(app)
jwt = JWTManager(app)
CORS(app)

with app.app_context():
    import models
    from models import Movie
    import json
    from pathlib import Path

    db.create_all()

    movies_file = Path(__file__).resolve().parent / "data" / "movies.json"

    with open(movies_file, "r", encoding="utf-8") as file:
        movies_data = json.load(file)

    for movie_data in movies_data:
        if not db.session.get(Movie, movie_data["id"]):
            db.session.add(Movie(**movie_data))

    db.session.commit()

def initialize_routes():
    from routes.auth import auth_bp
    from routes.movies import movie_bp
    from routes.watchlist import watchlist_bp
    from routes.watched import watched_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(movie_bp, url_prefix='/api/movies')
    app.register_blueprint(watchlist_bp, url_prefix='/api/watchlist')
    app.register_blueprint(watched_bp, url_prefix='/api/watched')
    
initialize_routes()

@app.route('/')
def home():
    return {"message": "Welcome to the Movie Watchlist API!"}, 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)