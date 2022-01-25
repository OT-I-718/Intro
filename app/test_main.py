'''
This is the unittest file.
Note: we are connecting to prod db for testing. This should be avoided by having a dev test db or mocking
'''
from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def test_read():
    response = client.get('/')
    assert response.status_code == 200


def test_write():
    response = client.put("/", json={'name': 'bazz', 'value': 5})
    assert response.status_code == 200
    # assert response.json() == {'bazz': 5}
    response = client.put("/", json={'name': 'bazz', 'value': 10})
    assert response.status_code == 422
    response = client.put("/", json={'name': 'Bazz', 'value': 5})
    assert response.status_code == 422
