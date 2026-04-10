from flask import Flask, g
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from extensions import redis_client

from config import Config
from db import init_db

from auth.login import login_bp
from auth.register import register_bp
from auth.logout import logout_bp
from routes.patients import patient_bp
from routes.doctors import doctor_bp
from routes.appointments import appointment_bp
from routes.admin import admin_bp
from routes.uploads import upload_bp

from middleware.rate_limiter import rate_limiter


app = Flask(__name__)
app.config.from_object(Config)

init_db(app)

CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

# JWT
app.config["JWT_BLOCKLIST_ENABLED"] = True
app.config["JWT_BLOCKLIST_TOKEN_CHECKS"] = ["access", "refresh"]

jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return redis_client.exists(jti) == 1

# Global Rate Limiter
app.before_request(rate_limiter)

# -----------------------------
# Register Blueprints
# -----------------------------
app.register_blueprint(login_bp, url_prefix="/auth")
app.register_blueprint(register_bp, url_prefix="/auth")
app.register_blueprint(logout_bp, url_prefix="/auth")

app.register_blueprint(patient_bp, url_prefix="/api")
app.register_blueprint(doctor_bp, url_prefix="/api")
app.register_blueprint(appointment_bp, url_prefix="/api")
app.register_blueprint(admin_bp, url_prefix="/api")
app.register_blueprint(upload_bp, url_prefix="/api")


# -----------------------------
# Rate Limit Headers
# -----------------------------
@app.after_request
def add_rate_limit_headers(response):
    if hasattr(g, "rate_limit"):
        response.headers["X-RateLimit-Limit"] = g.rate_limit
        response.headers["X-RateLimit-Remaining"] = g.remaining
    return response


# -----------------------------
# Health Check
# -----------------------------
@app.route("/")
def home():
    return {"message": "Hospital Backend Running 🚀"}

print(app.url_map)  # Debug: Print all registered routes


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)