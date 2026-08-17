from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

client = TestClient(app)


def setup_module(module):
    Base.metadata.create_all(bind=engine)


def test_create_and_get_doctor():
    payload = {"name": "Dr. Who", "specialization": "Time Travel"}
    r = client.post('/doctors/', json=payload)
    assert r.status_code == 201
    d = r.json()
    assert d['name'] == 'Dr. Who'

    r2 = client.get(f"/doctors/{d['id']}")
    assert r2.status_code == 200
    assert r2.json()['specialization'] == 'Time Travel'


def test_get_all_doctors():
    r = client.get('/doctors/')
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_get_missing_doctor():
    r = client.get('/doctors/999999')
    assert r.status_code == 404
