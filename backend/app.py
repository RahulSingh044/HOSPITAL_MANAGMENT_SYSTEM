from flask import Flask

from flask_jwt_extended import JWTManager

from config import Config

from auth import auth_bp

from routes.patients import patient_bp
from routes.doctors import doctor_bp
from routes.appointments import appointment_bp

from redis_client import redis_client

print("Testing Redis connection...")
print(redis_client.ping())

app = Flask(__name__)
app.config.from_object(Config)

jwt = JWTManager(app)

# zhi shi register blueprint, khong can url_prefix vi da co trong blueprint roi
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(patient_bp, url_prefix="/api")
app.register_blueprint(doctor_bp, url_prefix="/api")
app.register_blueprint(appointment_bp, url_prefix="/api")

@app.route("/")
def home():
    return {"message": "Hospital Backend Running 🚀"}

if __name__ == "__main__":
    app.run(debug=True)