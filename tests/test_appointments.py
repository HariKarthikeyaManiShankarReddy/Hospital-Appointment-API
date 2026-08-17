from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
import datetime

client = TestClient(app)

def setup_module(module):
    Base.metadata.create_all(bind=engine)

def test_create_and_get_appointment_and_overlap():
    # create patient
    p = client.post('/patients/', json={"name": "Bob", "email": "bob@example.com"}).json()
    # create doctor
    d = client.post('/doctors/', json={"name": "Dr. X"}).json()

    start1 = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
    end1 = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)).replace(microsecond=0).isoformat()
    appt1 = client.post('/appointments/', json={"patient_id": p['id'], "doctor_id": d['id'], "appointment_start": start1, "appointment_end": end1})
    assert appt1.status_code == 201

    # overlapping appointment (should be rejected)
    start2 = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)).replace(microsecond=0).isoformat()
    end2 = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1, minutes=30)).replace(microsecond=0).isoformat()
    appt2 = client.post('/appointments/', json={"patient_id": p['id'], "doctor_id": d['id'], "appointment_start": start2, "appointment_end": end2})
    assert appt2.status_code == 400

    # non-overlapping appointment (after end)
    start3 = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=2)).replace(microsecond=0).isoformat()
    end3 = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=3)).replace(microsecond=0).isoformat()
    appt3 = client.post('/appointments/', json={"patient_id": p['id'], "doctor_id": d['id'], "appointment_start": start3, "appointment_end": end3})
    assert appt3.status_code == 201

    # get all appointments
    r = client.get('/appointments/')
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_invalid_appointment_and_missing_appointment():
    p = client.post('/patients/', json={"name": "Dana", "email": "dana@example.com"}).json()
    d = client.post('/doctors/', json={"name": "Dr. Y"}).json()

    invalid = {
        "patient_id": p['id'],
        "doctor_id": d['id'],
        "appointment_start": "2026-08-20T12:00:00",
        "appointment_end": "2026-08-20T11:00:00",
    }
    r = client.post('/appointments/', json=invalid)
    assert r.status_code == 400

    r2 = client.get('/appointments/999999')
    assert r2.status_code == 404
