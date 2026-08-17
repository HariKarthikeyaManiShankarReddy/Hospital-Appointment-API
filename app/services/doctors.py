from sqlalchemy.orm import Session
from app.models.doctor import Doctor

def get_doctor(db: Session, doctor_id: int):
    return db.query(Doctor).filter(Doctor.id == doctor_id).first()

def get_doctors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Doctor).offset(skip).limit(limit).all()

def create_doctor(db: Session, name: str, specialization: str = None):
    doctor = Doctor(name=name, specialization=specialization)
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor
