from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import role_required
from db import mongo
from bson import ObjectId
from datetime import datetime

appointment_bp = Blueprint("appointments", __name__)


# ---------------------------------
# Patient books appointment
# ---------------------------------
@appointment_bp.route("/appointments", methods=["POST"])
@jwt_required()
@role_required("Patient")
def create_appointment():

    patient_id = get_jwt_identity()
    data = request.json

    appointment = {
        "patient_id": ObjectId(data["patient_id"]),
        "doctor_id": ObjectId(data["doctor_id"]),
        "date": datetime.strptime(data["date"], "%Y-%m-%d"),
        "status": "Scheduled"
    }

    mongo.db.appointments.insert_one(appointment)

    mongo.db.patients.update_one(
        {"_id": ObjectId(patient_id)},
        {"$set": {"last_visit": appointment["date"]}}
    )

    return jsonify({"message": "Appointment booked"}), 201


# ---------------------------------
# Admin view all appointments
# ---------------------------------
@appointment_bp.route("/appointments", methods=["GET"])
@jwt_required()
@role_required("Admin")
def get_all_appointments():

    appointments = list(mongo.db.appointments.find({}))

    for a in appointments:
        a["_id"] = str(a["_id"])
        a["patient_id"] = str(a["patient_id"])
        a["doctor_id"] = str(a["doctor_id"])

    return jsonify(appointments)


# ---------------------------------
# TEMP BULK APPOINTMENT INSERT
# ---------------------------------
from datetime import datetime
from bson import ObjectId

@appointment_bp.route("/appointments/bulk", methods=["POST"])
def bulk_appointments():

    data = request.json
    appointments = []

    for item in data:

        date = datetime.strptime(item["date"], "%Y-%m-%dT%H:%M:%S")

        appointment = {
            "patient_id": ObjectId(item["patient_id"]),
            "doctor_id": ObjectId(item["doctor_id"]),
            "date": date,
            "status": "Scheduled"
        }

        appointments.append(appointment)

        # update patient's last visit
        mongo.db.patients.update_one(
            {"_id": ObjectId(item["patient_id"])},
            {"$set": {"last_visit": date}}
        )

    mongo.db.appointments.insert_many(appointments)

    return jsonify({"message": "Bulk appointments created"}), 201