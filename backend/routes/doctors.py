from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from redis_client import redis_client

# zhi shi register blueprint, khong can url_prefix vi da co trong blueprint roi
doctor_bp = Blueprint("doctors", __name__)

@doctor_bp.route("/doctors", methods=["POST"])
@jwt_required()
def add_doctor():
    data = request.json
    doctor_id = redis_client.incr("doctor:id") # yuan zhi zeng jia shu qi, wei mei ge xin yue hui sheng cheng wei yi de shun xu ID

    redis_client.hset(f"doctor:{doctor_id}", mapping={
        "id": doctor_id,
        "name": data["name"],
        "specialization": data["specialization"]
    })

    return jsonify({"message": "Doctor added"}), 201


@doctor_bp.route("/doctors", methods=["GET"])
@jwt_required()
def get_doctors():
    keys = redis_client.keys("doctor:*")
    doctors = []

    for key in keys:
        doctors.append(redis_client.hgetall(key))

    return jsonify(doctors)