import pytest
from fastapi.testclient import TestClient
from app.main import app  # Supondo que o FastAPI esteja sendo inicializado no arquivo main.py

client = TestClient(app)

def test_login_success():
    response = client.post("/auth/login", json={"username": "user", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_credentials():
    response = client.post("/auth/login", json={"username": "invalid", "password": "invalid"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}

def test_protected_route_without_token():
    response = client.get("/protected-route")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_protected_route_with_token():
    # Primeiro, faça o login para obter o token
    login_response = client.post("/auth/login", json={"username": "user", "password": "password"})
    token = login_response.json()["access_token"]

    # Agora, faça a requisição para a rota protegida com o token
    response = client.get("/protected-route", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"message": "Access granted"}