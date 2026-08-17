from pydantic import BaseModel, EmailStr
from typing import Optional

class PatientCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None

class PatientRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: Optional[str] = None

    class Config:
        orm_mode = True
