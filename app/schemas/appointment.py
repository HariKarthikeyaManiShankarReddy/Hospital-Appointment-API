from pydantic import BaseModel
from datetime import datetime

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_start: datetime
    appointment_end: datetime

class AppointmentRead(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    appointment_start: datetime
    appointment_end: datetime

    class Config:
        orm_mode = True
