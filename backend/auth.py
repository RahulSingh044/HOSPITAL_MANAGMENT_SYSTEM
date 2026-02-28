from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from redis_client import redis_client

# zhi shi register blueprint, khong can url_prefix vi da co trong blueprint roi
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    user_id = redis_client.incr("user:id")

    redis_client.hset(f"user:{user_id}", mapping={
        "id": user_id,
        "name": data["name"],
        "email": data["email"],
        "password": generate_password_hash(data["password"])  # hash password before storing
    })

    return jsonify({"message": "User registered"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    keys = redis_client.keys("user:*")

    for key in keys:
        user = redis_client.hgetall(key)
        if user.get("email") == data["email"]:
            if check_password_hash(user["password"], data["password"]):
                token = create_access_token(identity=user["id"])
                return jsonify({"token": token})  # auth token generation

    return jsonify({"error": "Invalid credentials"}), 401