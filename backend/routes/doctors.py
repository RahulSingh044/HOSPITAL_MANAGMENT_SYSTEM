from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import role_required
from bson import ObjectId
from db import mongo

doctor_bp = Blueprint("doctors", __name__)

# Doctor profile
@doctor_bp.route("/doctors/me", methods=["GET"])
@jwt_required()
@role_required("Doctor")
def get_my_profile():
    user_id = get_jwt_identity()
    doctor = mongo.db.doctors.find_one({"_id": ObjectId(user_id)})

    if not doctor:
        return jsonify({"error": "Doctor profile not found"}), 404

    doctor["_id"] = str(doctor["_id"])
    return jsonify(doctor)


# Doctor appointments
@doctor_bp.route("/doctors/my-appointments", methods=["GET"])
@jwt_required()
@role_required("Doctor")
def my_appointments():
    user_id = get_jwt_identity()
    appointments = list(mongo.db.appointments.find({"doctor_id": user_id}))

    for a in appointments:
        a["_id"] = str(a["_id"])

    return jsonify(appointments)