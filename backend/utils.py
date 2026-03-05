from flask_jwt_extended import get_jwt
from functools import wraps
from flask import jsonify

def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()

            if claims.get("role") != required_role:
                return jsonify({"error": "Unauthorized"}), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper


from db import mongo
from pymongo import ReturnDocument

def get_next_medical_id():

    counter = mongo.db.counters.find_one_and_update(
        {"_id": "patient_id"},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )

    num = counter["seq"]

    return f"MR-{str(num).zfill(5)}"
    