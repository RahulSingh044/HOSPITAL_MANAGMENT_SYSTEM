from app import app
from db import mongo
from bson import ObjectId
from datetime import datetime

with app.app_context():
    # patients = mongo.db.patients.find({"age": {"$exists": False}})

    # for p in patients:
    #     agex = random.randint(18, 35)

    #     mongo.db.patients.update_one(
    #         {"_id": p["_id"]},
    #         {"$set": {"age": agex}}
    #     )

    mongo.db.appointments.delete_many({})

    print("Done")