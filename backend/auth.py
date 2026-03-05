from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from db import mongo
from utils import get_next_medical_id
from datetime import datetime

auth_bp = Blueprint("auth", __name__)

# -----------------------------
# Patient Register
# -----------------------------

@auth_bp.route("/register/patient", methods=["POST"])
def register_patient():

    data = request.json

    if mongo.db.patients.find_one({"email": data["email"]}):
        return jsonify({"error": "Email already exists"}), 400

    medical_id = get_next_medical_id()

    patient = {
        "medical_id": medical_id,
        "name": data["name"],
        "age": data["age"], 
        "gender": data["gender"],
        "mobile": data["mobile"],
        "admission_date": datetime.utcnow(),
        "condition": "Observing",
        "last_visit": None,
        "email": data["email"],
        "password": generate_password_hash(data["password"])
    }
    

    mongo.db.patients.insert_one(patient)

    return jsonify({
        "message": "Patient registered",
        "medical_id": medical_id
    }), 201


# -----------------------------
# Patient Register
# -----------------------------
@auth_bp.route("/register/bulk-patient", methods=["POST"])
def register_bulk_patient():

    data = request.json

    users = []

    for i in data:

        if mongo.db.patients.find_one({"email": i["email"]}):
            return jsonify({"error": "Email already exists"}), 400

        patient = {
            "name": i["name"],
            "gender": i["gender"],
            "mobile": i["mobile"],
            "email": i["email"],
            "password": generate_password_hash(i["password"])
        }

        users.append(patient)

    mongo.db.patients.insert_many(users)

    return jsonify({
        "message": "Patients registered",
        "count": len(patients)
    }), 201


# -----------------------------
# Patient Login
# -----------------------------
@auth_bp.route("/login/patient", methods=["POST"])
def login_patient():

    data = request.json

    user = mongo.db.patients.find_one({"email": data["email"]})

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=str(user["_id"]), additional_claims={"role": "Patient"})

    return jsonify({"token": token})


# -----------------------------
# Doctor Login
# -----------------------------
@auth_bp.route("/login/doctor", methods=["POST"])
def login_doctor():

    data = request.json

    user = mongo.db.doctors.find_one({"email": data["email"]})

    if not user:
        return jsonify({"error": "Doctor not found"}), 404

    if not check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=str(user["_id"]), additional_claims={"role": "Doctor"})

    return jsonify({"token": token})


# -----------------------------
# TEMP ADMIN REGISTER
# -----------------------------
@auth_bp.route("/register/admin", methods=["POST"])
def register_admin_temp():

    data = request.json

    if mongo.db.admins.find_one({"email": data["email"]}):
        return jsonify({"error": "Admin already exists"}), 400

    admin = {
        "name": data["name"],
        "email": data["email"],
        "password": generate_password_hash(data["password"])
    }

    mongo.db.admins.insert_one(admin)

    return jsonify({"message": "Admin created"}), 201

# -----------------------------
# ADMIN LOGIN
# -----------------------------
@auth_bp.route("/login/admin", methods=["POST"])
def login_admin():

    data = request.json

    user = mongo.db.admins.find_one({"email": data["email"]})

    if not user:
        return jsonify({"error": "Admin not found"}), 404

    if not check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(
        identity=str(user["_id"]),
        additional_claims={"role": "Admin"}
    )

    return jsonify({"token": token})