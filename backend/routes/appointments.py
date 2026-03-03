from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from redis_client import redis_client


# zhi shi register blueprint, khong can url_prefix vi da co trong blueprint roi
appointment_bp = Blueprint("appointments", __name__)

@appointment_bp.route("/appointments", methods=["POST"])
@jwt_required()
def add_appointment():
    data = request.json
    appointment_id = redis_client.incr("appointment:id") # yuan zhi zeng jia shu qi, wei mei ge xin yue hui sheng cheng wei yi de shun xu ID

    redis_client.hset(f"appointment:{appointment_id}", mapping={
        "id": appointment_id,
        "patient_id": data["patient_id"],
        "doctor_id": data["doctor_id"],
        "date": data["date"]
    })

    return jsonify({"message": "Appointment created"}), 201


@appointment_bp.route("/appointments", methods=["GET"])
@jwt_required()
def get_appointments():
    keys = redis_client.keys("appointment:[0-9]*") # kong keys = redis_client.keys("appointment:*") --- IGNORE --- 
    appointments = []

    for key in keys:
        appointments.append(redis_client.hgetall(key)) # hgetall se tra ve 1 dict, khong can chuyen doi nua

    return jsonify(appointments)