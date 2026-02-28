from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from redis_client import redis_client

patient_bp = Blueprint("patients", __name__)

@patient_bp.route("/patients", methods=["POST"])
@jwt_required()
def add_patient():
    data = request.json
    patient_id = redis_client.incr("patient:id")

    redis_client.hset(f"patient:{patient_id}", mapping={
        "id": patient_id,
        "name": data["name"],
        "age": data["age"],
        "mobile": data["mobile"]
    })

    return jsonify({"message": "Patient added"}), 201


@patient_bp.route("/patients", methods=["GET"])
@jwt_required()
def get_patients():
    keys = redis_client.keys("patient:[0-9]*")
    patients = []

    for key in keys:
        patients.append(redis_client.hgetall(key))

    return jsonify(patients)