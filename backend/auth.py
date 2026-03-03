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
        "password": generate_password_hash(data["password"])
    })

    redis_client.set(f"user:email:{data['email']}", user_id)

    return jsonify({"message": "User registered"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    # Validate required fields
    if not data or not data.get("email") or not data.get("password") or not data.get("role"):
        return jsonify({"error": "Email, password and role are required"}), 400

    # Get user ID from Redis using email
    user_id = redis_client.get(f"user:email:{data['email']}")

    if not user_id:
        return jsonify({"error": "Invalid credentials"}), 401

    # Get full user data
    user = redis_client.hgetall(f"user:{user_id}")

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    # Check password
    if not check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    # Check role matches registered role
    if user.get("role") != data["role"]:
        return jsonify({"error": "Role mismatch"}), 403

    # Generate JWT with role included
    token = create_access_token(
        identity=user["id"],
        additional_claims={"role": user["role"]}
    )

    return jsonify({
        "token": token,
        "role": user["role"]
    }), 200