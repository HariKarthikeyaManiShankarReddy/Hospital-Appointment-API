from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.patient import PatientCreate, PatientRead
from app.services import patients as patient_svc

router = APIRouter()

@router.get("/", response_model=list[PatientRead])
def list_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return patient_svc.get_patients(db, skip=skip, limit=limit)

@router.post("/", response_model=PatientRead, status_code=status.HTTP_201_CREATED)
def create_patient(payload: PatientCreate, db: Session = Depends(get_db)):
    try:
        patient = patient_svc.create_patient(db, name=payload.name, email=payload.email, phone=payload.phone)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return patient

@router.get("/{patient_id}", response_model=PatientRead)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = patient_svc.get_patient(db, patient_id=patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient
