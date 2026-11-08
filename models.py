from db import db
from sqlalchemy import String, Integer, ForeignKey, Text, DateTime, UniqueConstraint
from sqlalchemy.orm import mapped_column
from sqlalchemy import JSON
from datetime import datetime, timezone

class User(db.Model):
    __tablename__ = "users"
    
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    username = mapped_column(String(255), unique=True, nullable=False)
    email = mapped_column(String(255), unique=True, nullable=False)
    password_hash = mapped_column(String(255), nullable=False)
    created_at = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = mapped_column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc)
    )

    watchlists = db.relationship('Watchlist', back_populates='user', cascade="all, delete-orphan")
    reviews = db.relationship('Review', back_populates='user', cascade="all, delete-orphan")
    watched = db.relationship('Watched', back_populates='user', cascade="all, delete-orphan")


    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class Movie(db.Model):
    __tablename__ = "movies"
    
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    title = mapped_column(String(255), nullable=False)
    year = mapped_column(Integer, nullable=False)
    director = mapped_column(String(255), nullable=False)
    genres = mapped_column(JSON, nullable=False)
    rating = mapped_column(db.Float, nullable=True)
    duration = mapped_column(String(50), nullable=True)
    synopsis = mapped_column(Text, nullable=True)
    poster_url = mapped_column(String(500), nullable=True)
    cast = mapped_column(JSON, nullable=True)

    
    watchlists = db.relationship('Watchlist', back_populates='movie', cascade="all, delete-orphan")
    reviews = db.relationship('Review', back_populates='movie', cascade="all, delete-orphan")
    watched = db.relationship('Watched', back_populates='movie', cascade="all, delete-orphan")

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "year": self.year,
            "director": self.director,
            "genres": self.genres or [],
            "rating": self.rating,
            "duration": self.duration,
            "synopsis": self.synopsis,
            "poster_url": self.poster_url,
            "cast": self.cast or []
        }


class Watchlist(db.Model):
    __tablename__ = "watchlist"

    __table_args__ = ( UniqueConstraint("user_id", "movie_id", name="unique_user_watchlist_movie"),)
    
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    movie_id = mapped_column(Integer, ForeignKey('movies.id'), nullable=False)
    created_at = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))


    user = db.relationship('User', back_populates='watchlists')
    movie = db.relationship('Movie', back_populates='watchlists')

    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "movie_id": self.movie_id,
            "movie": self.movie.to_json() if self.movie else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class Watched(db.Model):
    __tablename__ = "watched"

    __table_args__ = (
        UniqueConstraint("user_id", "movie_id", name="unique_user_watched_movie"),
    )

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    movie_id = mapped_column(Integer, ForeignKey('movies.id'), nullable=False)
    watched_at = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', back_populates='watched')
    movie = db.relationship('Movie', back_populates='watched')

    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "movie_id": self.movie_id,
            "movie": self.movie.to_json() if self.movie else None,
            "watched_at": self.watched_at.isoformat() if self.watched_at else None
        }


class Review(db.Model):
    __tablename__ = "reviews"

    __table_args__ = (
        UniqueConstraint("user_id", "movie_id", name="unique_user_movie_review"),
    )
    
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    movie_id = mapped_column(Integer, ForeignKey('movies.id'), nullable=False)
    rating = mapped_column(Integer, nullable=False)      
    review = mapped_column(Text, nullable=True)         
    created_at = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = mapped_column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc)
    )

    user = db.relationship('User', back_populates='reviews')
    movie = db.relationship('Movie', back_populates='reviews')

    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "movie_id": self.movie_id,
            "rating": self.rating,
            "review": self.review,
            "movie": self.movie.to_json() if self.movie else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }