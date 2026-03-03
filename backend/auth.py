from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from db import mongo

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    # Prevent role injection from frontend
    role = "Patient"

    if mongo.db.users.find_one({"email": data["email"]}):
        return jsonify({"error": "Email already exists"}), 400

    user = {
        "name": data["name"],
        "role": role,
        "gender": data["gender"],
        "mobile": data["mobile"],
        "email": data["email"],
        "password": generate_password_hash(data["password"])
    }

    result = mongo.db.users.insert_one(user)

    # Create patient profile linked to user
    patient_profile = {
        "user_id": str(result.inserted_id),
        "name": data["name"],
        "gender": data["gender"],
        "mobile": data["mobile"]
    }

    mongo.db.patients.insert_one(patient_profile)

    return jsonify({"message": "Patient registered"}), 201



@auth_bp.route("/register/admin", methods=["POST"])
def add_admin():
    data = request.json
    
    role = "Admin"

    if mongo.db.users.find_one({"email": data["email"]}):
        return jsonify({"error": "Email already exists"}), 400

    user = {
        "name": data["name"],
        "role": role,
        "email": data["email"],
        "password": generate_password_hash(data["password"])
    }

    mongo.db.users.insert_one(user)

    return jsonify({"message": "admin created"}) , 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    user = mongo.db.users.find_one({"email": data["email"]})

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    if not check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(
        identity=str(user["_id"]),
        additional_claims={"role": user["role"]}
    )

    return jsonify({
        "token": token,
        "role": user["role"]
    })