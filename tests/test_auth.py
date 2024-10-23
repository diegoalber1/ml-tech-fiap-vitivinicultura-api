import pytest
from fastapi.testclient import TestClient
from app.main import app  # Importa a aplicação FastAPI

client = TestClient(app)

def test_login_success():
    response = client.post("/token", data={"username": "fiap", "password": "mltech"})  # Chama o endpoint correto
    assert response.status_code == 200
    assert "access_token" in response.json()  # Verifica se o token de acesso está presente

def test_login_invalid_credentials():
    response = client.post("/token", data={"username": "invalid", "password": "invalid"})
    assert response.status_code == 400  # Verifica se o status é 400 para credenciais inválidas
    assert response.json() == {"detail": "Credenciais inválidas"}  # Verifica a mensagem de erro

def test_protected_route_without_token():
    response = client.get("/users/me")  # Tenta acessar a rota protegida sem token
    assert response.status_code == 401  # Verifica se o status é 401 (não autenticado)
    assert response.json() == {"detail": "Not authenticated"}  # Verifica a mensagem de erro

def test_protected_route_with_token():
    # Primeiro, faça o login para obter o token
    login_response = client.post("/token", data={"username": "fiap", "password": "mltech"})
    token = login_response.json()["access_token"]

    # Agora, faça a requisição para a rota protegida com o token
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200  # Verifica se o status é 200
    assert response.json() == {"username": "fiap"}  # Verifica se o nome de usuário está correto
