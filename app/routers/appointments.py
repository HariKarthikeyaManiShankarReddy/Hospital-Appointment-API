from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.appointment import AppointmentCreate, AppointmentRead
from app.services import appointments as appt_svc

router = APIRouter()

@router.get("/", response_model=list[AppointmentRead])
def list_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return appt_svc.get_appointments(db, skip=skip, limit=limit)

@router.post("/", response_model=AppointmentRead, status_code=status.HTTP_201_CREATED)
def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_db)):
    try:
        appt = appt_svc.create_appointment(db, patient_id=payload.patient_id, doctor_id=payload.doctor_id, start=payload.appointment_start, end=payload.appointment_end)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return appt

@router.get("/{appointment_id}", response_model=AppointmentRead)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appt = appt_svc.get_appointment(db, appointment_id=appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt
