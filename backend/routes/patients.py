from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import role_required
from bson import ObjectId
from db import mongo

patient_bp = Blueprint("patients", __name__)

# Patient profile
@patient_bp.route("/patients/me", methods=["GET"])
@jwt_required()
@role_required("Patient")
def get_my_profile():
    user_id = get_jwt_identity()
    patient = mongo.db.patients.find_one({"_id": ObjectId(user_id)})

    if not patient:
        return jsonify({"error": "Patient profile not found"}), 404

    patient["_id"] = str(patient["_id"])
    return jsonify(patient)


# Update patient profile
@patient_bp.route("/patients/update", methods=["PUT"])
@jwt_required()
@role_required("Patient")
def update_patient():
    user_id = get_jwt_identity()
    data = request.json

    mongo.db.patients.update_one(
        {"user_id": user_id},
        {"$set": data}
    )

    return jsonify({"message": "Profile updated"})