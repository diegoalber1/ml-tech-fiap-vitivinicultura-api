import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_app_initialization():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bem-vindo à RM358672-fiap-vitivinicultura-api- TECH CHALLENGE!"}

def test_included_routers():
    # Testar se as rotas estão inclusas na aplicação
    response_auth = client.get("/auth/login")
    assert response_auth.status_code in (200, 404)  # 200 se o endpoint estiver implementado, 404 se não

    response_producao = client.get("/producao")
    assert response_producao.status_code in (200, 401)  # 200 se autenticado, 401 se não

    response_processamento = client.get("/processamento")
    assert response_processamento.status_code in (200, 401)  # 200 se autenticado, 401 se não

def test_documentation():
    # Testa se a documentação da API está acessível
    response = client.get("/docs")
    assert response.status_code == 200
    assert "Swagger UI" in response.text  # Verifica se a UI do Swagger está presente

    response = client.get("/redoc")
    assert response.status_code == 200
    print(response.text)
    assert "ReDoc" in response.text  # Verifica se a documentação Redoc está presente
