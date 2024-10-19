import pytest
from fastapi.testclient import TestClient
from app.main import app  # Supondo que o FastAPI esteja sendo inicializado no arquivo main.py

client = TestClient(app)

def test_get_producao():
    response = client.get("/producao")
    assert response.status_code == 200
    assert "headers" in response.json()
    assert "rows" in response.json()

def test_get_processamento():
    response = client.get("/processamento")
    assert response.status_code == 200
    assert "headers" in response.json()
    assert "rows" in response.json()

def test_get_invalid_section():
    response = client.get("/invalid_section")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}