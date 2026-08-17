import os
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

client = TestClient(app)


def setup_module(module):
    # ensure fresh test database
    Base.metadata.create_all(bind=engine)


def teardown_module(module):
    # remove DB file used for tests if sqlite file
    url = os.getenv('DATABASE_URL', 'sqlite:///./hospital.db')
    if url.startswith('sqlite:///'):
        path = url.replace('sqlite:///','')
        try:
            os.remove(path)
        except Exception:
            pass


def test_create_and_get_patient():
    payload = {"name": "Alice", "email": "alice@example.com", "phone": "12345"}
    r = client.post('/patients/', json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data['name'] == 'Alice'

    r2 = client.get(f"/patients/{data['id']}")
    assert r2.status_code == 200
    assert r2.json()['email'] == 'alice@example.com'


def test_get_all_patients():
    r = client.get('/patients/')
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_get_missing_patient_and_duplicate_email():
    payload = {"name": "Charlie", "email": "charlie@example.com", "phone": "54321"}
    r = client.post('/patients/', json=payload)
    assert r.status_code == 201

    r2 = client.get('/patients/999999')
    assert r2.status_code == 404

    r3 = client.post('/patients/', json=payload)
    assert r3.status_code == 400
