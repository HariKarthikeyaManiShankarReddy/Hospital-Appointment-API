Hospital Appointment API

Overview
- FastAPI application providing CRUD-like endpoints for Patients, Doctors and Appointments.
- Prevents overlapping appointments for the same doctor.
- Uses SQLAlchemy for ORM and Alembic for migrations.
- Poetry for dependency management.
- CI workflow (GitHub Actions) runs ruff linting, bandit security checks, pytest with coverage, and publishes Docker image to Docker Hub.

Running locally
1. Install dependencies with poetry:
   poetry install
2. Start the app:
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Database
- Default uses SQLite file `hospital.db`. Set DATABASE_URL env var to change the DB.
- Alembic migrations included under alembic/ (initial revision 0001_initial.py).

API endpoints (three operations per model):
Patients - GET /patients (list), POST /patients (create), GET /patients/{id}
Doctors  - GET /doctors (list), POST /doctors (create), GET /doctors/{id}
Appointments - GET /appointments (list), POST /appointments (create), GET /appointments/{id}

Business rule
- Overlapping appointments for the same doctor are rejected using the condition:
  existing_start < new_end AND existing_end > new_start

Testing
- Tests located in tests/ use pytest and FastAPI TestClient.

Migrations
- Alembic is configured in alembic/. To create and apply migrations locally:
  - alembic -c alembic.ini revision --autogenerate -m "message"
  - alembic -c alembic.ini upgrade head

CI
- GitHub Actions workflow at .github/workflows/ci.yml runs ruff, bandit, pytest (with coverage and a fail-under threshold of 85%), and publishes to Docker Hub when on the main branch.
- To allow Docker Hub publishing, set repository secrets: DOCKERHUB_USERNAME and DOCKERHUB_TOKEN.

Notes
- Alembic can be used for proper schema migrations. For convenience, the app currently runs Base.metadata.create_all() at startup so the app is runnable out of the box for local development.
