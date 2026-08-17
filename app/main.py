from fastapi import FastAPI
from app.routers import patients, doctors, appointments
from app.database import engine, Base

app = FastAPI(title="Hospital Appointment API")

# Create tables at startup so the app can run out-of-the-box for development/testing.
# Alembic is included for proper migrations; create_all is a convenience for local runs.
Base.metadata.create_all(bind=engine)

app.include_router(patients.router, prefix="/patients", tags=["patients"])
app.include_router(doctors.router, prefix="/doctors", tags=["doctors"])
app.include_router(appointments.router, prefix="/appointments", tags=["appointments"])