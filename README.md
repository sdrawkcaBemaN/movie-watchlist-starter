# FilmLog

## Overview

FilmLog is a movie watchlist and review platform that lets users find movies and manage their watchlists, watched movies, and also write their own reviews. This application also uses Google Gemini AI to give personal reccomendations based on a user prompt.

## Live Demo

Website: https://movie-watchlist-starter-frontend-mcl4p1b3g-gooners25.vercel.app/
Backend API: https://filmlog-five.vercel.app/
API Testing: You can use Postman to access the API endpoints documented below.

## Tech Stack

### Backend

- **Python** - Main programming language
- **Flask** - REST API framework
- **Flask SQL Alchemy** - ORM for flask
- **SQLite** - Relational database
- **JWT** - Authentication and protecting routes
- **Bcrypt** - Password hashing
- **Gemini API** - AI movie reccomendations

## Project Structure

```text
movie-watchlist-starter/
├── app.py # Main Flask application
├── db.py # SQLAlchemy database configuration
├── models.py # Database models and relationships
├── requirements.txt # Dependencies and requirements
├── .env # Environment variables (not committed)
├── .gitignore # Ignored files
├── README.md
│
├── data/
│ ├── movies.json # Initial movie dataset (20 movies)
│ └── seed.sql # Initial SQL seed data
│
├── routes/ # Routes and endpoints
│ ├── **init**.py
│ ├── auth.py
│ ├── movies.py
│ ├── watchlist.py
│ └── watched.py
│
└── frontend/
├── index.html
├── app.js
└── README.md
```

## Prerequisites

- **Python**
- **Git** – To clone the repository.
- **Google Gemini API Key** – For the AI reccomendations.
- **Postman (optional)** – For testing API endpoints.

## Installation

To run it locally just

1. Copy the repo.
   git clone <https://github.com/sdrawkcaBemaN/movie-watchlist-starter>

2. Create and active your venv in the project directory.
   python -m venv venv
   venv\Scripts\activate

3. Install dependencies.
   pip install -r requirements.txt

## Environment Variables

- API_KEY = [your Gemini API key]
- JWT_SECRET_KEY = [your secret key]

## Running the Application

To start the application

1. Run the flask backend.
   python app.py

Running the app already intializes the database.

2. Open the frontend.

## API Endpoints

- POST `/api/auth/register`
- POST `/api/auth/login`
- GET `/api/movies/`
- GET `/api/movies/<id>`
- POST `/api/movies/recommend`
- GET `/api/watchlist/`
- POST `/api/watchlist/`
- DELETE `/api/watchlist/<movie_id>`
- GET `/api/watched/`
- POST `/api/watched/`
