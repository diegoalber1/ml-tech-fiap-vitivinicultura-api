import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_app_initialization():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Vitivinicultura API"}