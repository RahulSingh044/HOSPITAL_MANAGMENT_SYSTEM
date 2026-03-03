from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import role_required
from db import mongo

appointment_bp = Blueprint("appointments", __name__)

# Patient books appointment
@appointment_bp.route("/appointments", methods=["POST"])
@jwt_required()
@role_required("Patient")
def create_appointment():
    user_id = get_jwt_identity()
    data = request.json

    appointment = {
        "patient_id": user_id,
        "doctor_id": data["doctor_id"],
        "date": data["date"],
        "status": "Scheduled"
    }

    mongo.db.appointments.insert_one(appointment)

    return jsonify({"message": "Appointment booked"}), 201


# Admin view all appointments
@appointment_bp.route("/appointments", methods=["GET"])
@jwt_required()
@role_required("Admin")
def get_all_appointments():
    appointments = list(mongo.db.appointments.find({}))

    for a in appointments:
        a["_id"] = str(a["_id"])

    return jsonify(appointments)