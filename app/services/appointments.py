from sqlalchemy.orm import Session
from app.models.appointment import Appointment
from datetime import datetime

def get_appointment(db: Session, appointment_id: int):
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()

def get_appointments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Appointment).offset(skip).limit(limit).all()

def overlapping_exists(db: Session, doctor_id: int, start: datetime, end: datetime) -> bool:
    # existing_start < new_end AND existing_end > new_start
    return db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        Appointment.appointment_start < end,
        Appointment.appointment_end > start
    ).first() is not None

def create_appointment(db: Session, patient_id: int, doctor_id: int, start: datetime, end: datetime):
    if start >= end:
        raise ValueError("appointment_start must be before appointment_end")
    if overlapping_exists(db, doctor_id, start, end):
        raise ValueError("appointment overlaps with existing appointment for this doctor")
    appointment = Appointment(patient_id=patient_id, doctor_id=doctor_id, appointment_start=start, appointment_end=end)
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment
