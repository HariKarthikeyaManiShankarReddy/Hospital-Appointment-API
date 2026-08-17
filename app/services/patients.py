from sqlalchemy.orm import Session
from app.models.patient import Patient

def get_patient(db: Session, patient_id: int):
    return db.query(Patient).filter(Patient.id == patient_id).first()

def get_patients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Patient).offset(skip).limit(limit).all()

def create_patient(db: Session, name: str, email: str, phone: str = None):
    patient = Patient(name=name, email=email, phone=phone)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient
