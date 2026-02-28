from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from redis_client import redis_client

# zhi shi register blueprint, khong can url_prefix vi da co trong blueprint roi
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    if redis_client.exists(f"user:email:{data['email']}"):
        return jsonify({"error": "Email already registered"}), 400
    
    user_id = redis_client.incr("user:id")

    redis_client.hset(f"user:{user_id}", mapping={
        "id": user_id,
        "name": data["name"],
        "role": data["role"],
        "gender": data["gender"],
        "mobile": data["mobile"],
        "email": data["email"],
        "password": generate_password_hash(data["password"])  # hash password before storing
    })

    redis_client.set(f"user:email:{data['email']}", user_id)

    return jsonify({"message": "User registered"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    user_id = redis_client.get(f"user:email:{data['email']}")

    if not user_id:
        return jsonify({"error": "Invalid credentials"}), 401

    user = redis_client.hgetall(f"user:{user_id}")

    if check_password_hash(user["password"], data["password"]):
        token = create_access_token(identity=user["id"])
        return jsonify({"token": token})  # auth token generation

    return jsonify({"error": "Invalid credentials"}), 401