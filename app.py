import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from db import db
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///watchlist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-fallback-key')

db.init_app(app)
jwt = JWTManager(app)
CORS(app)

with app.app_context():
    import models 
    db.create_all()

@app.route('/')
def home():
    return {"message": "Welcome to the Movie Watchlist API!"}, 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)