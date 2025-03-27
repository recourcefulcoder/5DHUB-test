from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_hello_wold():
    response = client.get("/hello-world")
    assert response.status_code == 200
    assert {"message": "Hello, world!"} == response.json()
