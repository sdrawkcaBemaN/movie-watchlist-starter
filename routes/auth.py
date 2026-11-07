from flask import Blueprint, request
from models import User
from db import db
import bcrypt
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)

# POST /api/auth/register
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return {"error": "Username, email, and password are required"}, 400

    user_exists = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()

    if user_exists:
        return {"error": "Username or email already exists"}, 409

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    new_user = User(
        username=username,
        email=email,
        password_hash=password_hash
    )
    db.session.add(new_user)
    db.session.commit()

    return {
        "message": "Registered successfully",
        "user": new_user.to_json()
    }, 201


# POST /api/auth/login
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"error": "Username and password are required"}, 400

    user = User.query.filter_by(username=username).first()

    if not user:
        return {"error": "Invalid username or password"}, 401

    password_valid = bcrypt.checkpw(
        password.encode("utf-8"),
        user.password_hash.encode("utf-8")
    )

    if not password_valid:
        return {"error": "Invalid username or password"}, 401
    
    access_token = create_access_token(identity=str(user.id))

    return {
        "message": "Login successful",
        "access_token": access_token,
        "user": user.to_json()
    }, 200