import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.auth import create_access_token

client = TestClient(app)

@pytest.fixture
def valid_token():
    token = create_access_token(data={"sub": "fiap"})
    return f"Bearer {token}"  # Certifique-se de que o token está prefixado corretamente

def test_get_producao(valid_token):
    response = client.get("/producao", headers={"Authorization": valid_token})
    print(response.status_code)
    print(response.json())  # Adiciona esta linha para ver a resposta completa
    # assert response.status_code == 200
    # assert "headers" in response.json()
    # assert isinstance(response.json().get("data"), list)


