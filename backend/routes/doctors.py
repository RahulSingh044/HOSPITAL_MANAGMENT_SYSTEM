from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func, or_
from utils import role_required
from extensions import db
from models import Doctor, Patient, Appointment, MedicalRecord, Prescription, Note, Vital
from datetime import date, datetime, timedelta

doctor_bp = Blueprint("doctors", __name__)

# -----------------------------
# Doctor Profile
# -----------------------------
@doctor_bp.route("/doctors/me", methods=["GET"])
@jwt_required()
@role_required("Doctor")
def get_my_profile():
    user_id = int(get_jwt_identity())
    doctor = Doctor.query.get(user_id)

    if not doctor:
        return jsonify({"error": "Doctor profile not found"}), 404

    doctor_dict = {
        "_id": str(doctor.id),
        "doctor_id": doctor.doctor_id,
        "name": doctor.name,
        "email": doctor.email,
        "specialization": doctor.specialization,
        "experience": doctor.experience,
        "schedule": doctor.schedule,
        "status": doctor.status,
        "mobile": doctor.mobile,
        "gender": doctor.gender,
        "image": doctor.image_url if doctor.image_url else f"https://ui-avatars.com/api/?name={doctor.name}"
    }
    return jsonify(doctor_dict)


# Todays dashboard
@doctor_bp.route("/doctors/dashboard", methods=["GET"])
@jwt_required()
@role_required("Doctor")
def doctor_dashboard():
    doctor_id = int(get_jwt_identity())

    # For today filtering, start and end of day datetime objects
    now = datetime.utcnow()
    start_of_today = datetime(now.year, now.month, now.day)
    
    # Weekly schedule from Monday (0) to Sunday (6) of current week
    start_of_week = start_of_today - timedelta(days=start_of_today.weekday())
    end_of_week = start_of_week + timedelta(days=7)

    # 1. Weekly appointments
    appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor_id,
        Appointment.status != "Cancelled",
        Appointment.date >= start_of_week,
        Appointment.date < end_of_week
    ).order_by(Appointment.date.asc()).all()
    
    weekly_schedule = []
    for appt in appointments:
        if appt.patient:
            weekly_schedule.append({
                "_id": str(appt.id),
                "patient_id": str(appt.patient_id),
                "doctor_id": str(appt.doctor_id),
                "status": appt.status,
                "type": appt.type if appt.type else "Consultation",
                "date": appt.date.strftime("%Y-%m-%d") if appt.date else "",
                "time": appt.date.strftime("%H:%M") if appt.date else "",
                "patient_name": appt.patient.name,
                "patient_age": appt.patient.age,
                "patient_gender": appt.patient.gender
            })
            
    today_str = start_of_today.strftime("%Y-%m-%d")
    today_appointments = [appt for appt in weekly_schedule if appt.get("date") == today_str]

    # 2. Total patients count
    total_patients = Patient.query.count()

    # 3. Pending reports count
    # pending_reports = MedicalRecord.query.filter_by(doctor_id=doctor_id, status="Pending").count()

    # 4. Recent patients
    recent = (
        Appointment.query.filter(
            Appointment.doctor_id == doctor_id,
            Appointment.status == "Completed",
            Appointment.date == start_of_today,
        )
        .order_by(Appointment.date.desc())
        .limit(5)
        .all()
    )

    recent_patients = []
    for appt in recent:
        if appt.patient:
            recent_patients.append({
                "_id": str(appt.patient.id),
                "medical_id": appt.patient.medical_id,
                "name": appt.patient.name,
                "age": appt.patient.age, 
            })

    return jsonify({
        "today_appointments": len(today_appointments),
        "appointments": today_appointments,
        "weekly_schedule": weekly_schedule,
        "total_patients": total_patients,
        # "pending_reports": pending_reports,
        "recent_patients": recent_patients
    })




# -----------------------------
# Doctor All Appointments
# -----------------------------
@doctor_bp.route("/doctors/my-appointments", methods=["GET"])
@jwt_required()
@role_required("Doctor")
def my_appointments():
    doctor_id = int(get_jwt_identity())

    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Filters
    search = request.args.get("search", type=str)
    status = request.args.get("status", type=str)

    # Base query
    query = Appointment.query.join(Patient).filter(Appointment.doctor_id == doctor_id, Appointment.status != "Completed", Appointment.status != "Cancelled")

    # Status filtering
    if status == "Today":
        today_str = date.today().strftime("%Y-%m-%d")
        query = query.filter(func.date(Appointment.date) == today_str)
    elif status:
        query = query.filter(Appointment.status == status)

    # Search filtering
    if search:
        query = query.filter(
            or_(
                Patient.name.ilike(f"%{search}%"),
                Patient.medical_id.ilike(f"%{search}%")
            )
        )

    # Pagination & ordering
    pagination = query.order_by(Appointment.date.asc()).paginate(page=page, per_page=per_page, error_out=False)

    # Format response
    formatted_appointments = [
        {
            "_id": str(appt.id),
            "patient_id": str(appt.patient_id),
            "doctor_id": str(appt.doctor_id),
            "status": appt.status,
            "type": appt.type if appt.type else "Consultation",
            "date": appt.date.strftime("%Y-%m-%d") if appt.date else "",
            "time": appt.date.strftime("%H:%M") if appt.date else "",
            "patient_name": appt.patient.name,
            "patient_age": appt.patient.age,
            "patient_gender": appt.patient.gender,
            "medical_id": appt.patient.medical_id
        }
        for appt in pagination.items
    ]

    return jsonify({
        "pagination": {
            "current_page": page,
            "per_page": per_page,
            "total_items": pagination.total,
            "total_pages": pagination.pages
        },
        "data": formatted_appointments
    })

# -----------------------------
# Doctor All Patients
# -----------------------------
@doctor_bp.route("/doctors/patients", methods=["GET"])
@jwt_required()
@role_required("Doctor")
def get_patients():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    search = request.args.get("search")
    patient_filter = request.args.get("filter")

    query = Patient.query
    if patient_filter and patient_filter != "All Patients":
        query = query.filter(Patient.condition == patient_filter)
    if search:
        query = query.filter(db.or_(
            Patient.name.ilike(f"%{search}%"),
            Patient.medical_id.ilike(f"%{search}%"),
            Patient.condition.ilike(f"%{search}%")
        ))
    
    query = query.filter()
        
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    patients = []
    for p in pagination.items:
        patients.append({
            "_id": str(p.id),
            "medical_id": p.medical_id,
            "name": p.name,
            "gender": p.gender,
            "age": p.age,
            "condition": p.condition,
            "email": p.email,
            "mobile": p.mobile,
            "last_visit": p.last_visit.strftime("%Y-%m-%d") if p.last_visit else None,
            "admission_date": p.admission_date.strftime("%Y-%m-%d") if p.admission_date else None
        })

    return jsonify({
        "pagination": {
            "current_page": page,
            "per_page": per_page,
            "total_items": pagination.total,
            "total_pages": pagination.pages
        },
        "data": patients
    })




# -----------------------------
# Single Patient Profile
# -----------------------------
@doctor_bp.route("/doctors/patient-profile/<patient_id>", methods=["GET"])
@jwt_required()
@role_required("Doctor")
def patient_profile(patient_id):
    if patient_id.startswith("MR-"):
        patient = Patient.query.filter_by(medical_id=patient_id).first()
    else:
        patient = Patient.query.get(int(patient_id))
    if not patient:
        return jsonify({"error": "Patient not found"}), 404
    bp_vital = Vital.query.filter_by(patient_id=patient.id, label="Blood Pressure").order_by(Vital.id.desc()).first()
    hr_vital = Vital.query.filter_by(patient_id=patient.id, label="Heart Rate").order_by(Vital.id.desc()).first()
    
    blood_pressure_str = f"{bp_vital.value} {bp_vital.unit or ''}".strip() if bp_vital else None
    heart_rate_str = f"{hr_vital.value} {hr_vital.unit or ''}".strip() if hr_vital else None
    
    appointments = Appointment.query.filter_by(patient_id=patient.id).all()
    appt_ids = [apt.id for apt in appointments]
    prescriptions = []
    if appt_ids:
        prescs = Prescription.query.filter(Prescription.appointment_id.in_(appt_ids)).order_by(Prescription.id.desc()).all()
        for pr in prescs:
            prescriptions.append({
                "name": pr.name,
                "dosage": pr.dosage,
                "frequency": pr.frequency,
                "duration": pr.duration
            })
            
    all_records = MedicalRecord.query.filter_by(patient_id=patient.id).order_by(MedicalRecord.date.desc(), MedicalRecord.id.desc()).all()
    medical_records = [{
        "id": mr.id,
        "date": mr.date,
        "title": mr.title,
        "description": mr.description,
        "appointment_id": mr.appointment_id
    } for mr in all_records]
        
    return jsonify({
        "_id": str(patient.id),
        "medical_id": patient.medical_id,
        "name": patient.name,
        "age": patient.age,
        "gender": patient.gender,
        "condition": patient.condition,
        "last_visit": patient.last_visit.isoformat() if patient.last_visit else None,
        "admission_date": patient.admission_date.isoformat() if patient.admission_date else None,
        "dob": patient.dob,
        "blood_type": patient.blood_type,
        "blood_pressure": blood_pressure_str,
        "heart_rate": heart_rate_str,
        "prescriptions": prescriptions,
        "recent_medical_records": medical_records
    })
   
# -----------------------------
# Patient Condition Update
# -----------------------------
@doctor_bp.route("/patients/<patient_id>/condition", methods=["PUT"])
@jwt_required()
@role_required("Doctor")
def update_condition(patient_id):
    if patient_id.startswith("MR-"):
        patient = Patient.query.filter_by(medical_id=patient_id).first()
    else:
        patient = Patient.query.get(int(patient_id))
    if not patient:
        return jsonify({"error": "Patient not found"}), 404
        
    data = request.json
    patient.condition = data.get("condition", "")
    db.session.commit()
    return jsonify({"message": "Patient condition updated"},)




# -----------------------------
# Add Prescription
# -----------------------------
@doctor_bp.route("/doctors/appointments/<apt_id>/prescription", methods=["POST"])
@jwt_required()
@role_required("Doctor")
def add_prescription(apt_id):
    apt = Appointment.query.get(int(apt_id))
    if not apt: 
        return jsonify({"error": "Appointment not found"}), 404
        
    data = request.json
    created_prescriptions = []
    for items in data:
        name = items.get("name")
        dosage = items.get("dosage")
        frequency = items.get("frequency")
        duration = items.get("duration")

        if not name or not dosage or not frequency or not duration:
            return jsonify({"error": "name and dosage are required for each prescription item"}), 400
        
        p = Prescription(
            appointment_id=apt.id,
            patient_id=apt.patient_id,
            name=name,
            dosage=dosage,
            frequency=frequency,
            duration=duration
        )
        db.session.add(p)
        created_prescriptions.append(p)

    db.session.commit()
    return jsonify({"message": "Prescription added successfully", "ids": [p.id for p in created_prescriptions]}), 201


# -----------------------------
# Add Note
# -----------------------------
@doctor_bp.route("/doctors/appointments/<apt_id>/note", methods=["POST"])
@jwt_required()
@role_required("Doctor")
def add_note(apt_id):
    apt = Appointment.query.get(int(apt_id))
    if not apt: 
        return jsonify({"error": "Appointment not found"}), 404
        
    data = request.json
    n = Note(
        appointment_id=apt.id,
        text=data.get("text"),
        patient_id=apt.patient_id,
        date=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    )
    db.session.add(n)
    db.session.commit()
    return jsonify({"message": "Note added successfully", "id": n.id}), 201

# -----------------------------
# Add Vital
# -----------------------------
@doctor_bp.route("/doctors/appointments/<apt_id>/vital", methods=["POST"])
@jwt_required()
@role_required("Doctor")
def add_vital(apt_id):
    apt = Appointment.query.get(int(apt_id))
    if not apt: 
        return jsonify({"error": "Appointment not found"}), 404
        
    vitals_data = request.json
    created_vitals = []

    for item in vitals_data:
        label = item.get("label")
        value = item.get("value")
        unit = item.get("unit")

        # Optional validation
        if not label or not value:
            return jsonify({"error": "label and value are required"}), 400

        v = Vital(
            appointment_id=apt.id,
            patient_id=apt.patient_id,
            label=label,
            value=value,
            unit=unit
        )
        db.session.add(v)
        created_vitals.append(v)

    db.session.commit()

    return jsonify({
        "message": "Vitals added successfully",
        "ids": [v.id for v in created_vitals]
    }), 201

# -----------------------------
# Add Medical Record (Unified History/Timeline API)
# -----------------------------
@doctor_bp.route("/doctors/appointments/<apt_id>/medical-record", methods=["POST"])
@jwt_required()
@role_required("Doctor")
def add_medical_record(apt_id):
    apt = Appointment.query.get(int(apt_id))
    if not apt:
        return jsonify({"error": "Appointment not found"}), 404

    doctor_id = int(get_jwt_identity())
    doctor = Doctor.query.get(doctor_id)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    # --- Fields ---
    title = data.get("title")
    description = data.get("description")

    # --- Date ---
    try:
        date_str = data.get("date")
        date = datetime.strptime(date_str, "%Y-%m-%d") if date_str else datetime.utcnow()
    except:
        return jsonify({"error": "Invalid date format"}), 400

    # --- Arrays of IDs ---
    vital_ids = data.get("vital_ids", [])
    note_ids = data.get("note_ids", [])
    prescription_ids = data.get("prescription_ids", [])

    # --- Get or create record ---
    record = MedicalRecord.query.filter_by(appointment_id=apt.id).first()

    if not record:
        record = MedicalRecord(
            patient_id=apt.patient_id,
            doctor_id=doctor.id,
            appointment_id=apt.id,
            date=date,
            title=title,
            description=description
        )
        db.session.add(record)
        db.session.commit()
        status_code = 201
    else:
        record.title = title
        record.description = description
        record.date = date
        status_code = 200

    # --- LINK VITALS ---
    for vid in vital_ids:
        v = Vital.query.get(vid)
        if v:
            v.medical_record_id = record.id

    # --- LINK NOTES ---
    for nid in note_ids:
        n = Note.query.get(nid)
        if n:
            n.medical_record_id = record.id

    # --- LINK PRESCRIPTIONS ---
    for pid in prescription_ids:
        p = Prescription.query.get(pid)
        if p:
            p.medical_record_id = record.id

    # --- Update appointment ---
    apt.diagnosisTitle = data.get("primary_diagnosis", title)
    apt.diagnosisDesc = data.get("symptoms", description)

    apt.status = "Completed"
    db.session.commit()

    return jsonify({
        "message": "Medical record saved successfully",
        "record_id": record.id
    }), status_code



