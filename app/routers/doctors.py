from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.doctor import DoctorCreate, DoctorRead
from app.services import doctors as doctor_svc

router = APIRouter()

@router.get("/", response_model=list[DoctorRead])
def list_doctors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return doctor_svc.get_doctors(db, skip=skip, limit=limit)

@router.post("/", response_model=DoctorRead, status_code=status.HTTP_201_CREATED)
def create_doctor(payload: DoctorCreate, db: Session = Depends(get_db)):
    try:
        doctor = doctor_svc.create_doctor(db, name=payload.name, specialization=payload.specialization)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return doctor

@router.get("/{doctor_id}", response_model=DoctorRead)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = doctor_svc.get_doctor(db, doctor_id=doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor
