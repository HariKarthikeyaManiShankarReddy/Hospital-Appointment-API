from pydantic import BaseModel
from typing import Optional

class DoctorCreate(BaseModel):
    name: str
    specialization: Optional[str] = None

class DoctorRead(BaseModel):
    id: int
    name: str
    specialization: Optional[str] = None

    class Config:
        orm_mode = True
