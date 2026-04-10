from flask import Blueprint, jsonify, current_app
from extensions import redis_client
from flask_jwt_extended import jwt_required, get_jwt

logout_bp = Blueprint("logout", __name__)

@logout_bp.route('/logout', methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]

    # Convert expiry to seconds if it's timedelta
    expires = current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
    if hasattr(expires, "total_seconds"):
        expires = int(expires.total_seconds())

    redis_client.set(jti, "revoked", ex=expires)

    return jsonify({"message": "Logout successful"}), 200