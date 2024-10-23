import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.auth import create_access_token
from unittest.mock import patch

client = TestClient(app)

@pytest.fixture
def valid_token():
    token = create_access_token(data={"sub": "fiap"})
    return f"Bearer {token}"

# Testes para a rota /producao
@patch('app.routes.get_data')
def test_get_producao(mock_get_data, valid_token):
    mock_get_data.return_value = {"data": ["vinho1", "vinho2"]}
    
    response = client.get("/producao", headers={"Authorization": valid_token})
    
    mock_get_data.assert_called_once_with("producao", None)  # Verifica se foi chamado com os parâmetros corretos
    
    assert response.status_code == 200
    assert "data" in response.json()
    assert isinstance(response.json()["data"], list)

# Testes para a rota /processamento
@patch('app.routes.get_data')
def test_get_processamento(mock_get_data, valid_token):
    mock_get_data.return_value = {"data": ["processo1", "processo2"]}
    
    response = client.get("/processamento", headers={"Authorization": valid_token})
    
    mock_get_data.assert_called_once_with("processamento", None)
    
    assert response.status_code == 200
    assert "data" in response.json()
    assert isinstance(response.json()["data"], list)

# Testes para a rota /comercializacao
@patch('app.routes.get_data')
def test_get_comercializacao(mock_get_data, valid_token):
    mock_get_data.return_value = {"data": ["comercial1", "comercial2"]}
    
    response = client.get("/comercializacao", headers={"Authorization": valid_token})
    
    mock_get_data.assert_called_once_with("comercializacao", None)
    
    assert response.status_code == 200
    assert "data" in response.json()
    assert isinstance(response.json()["data"], list)

# Testes para a rota /importacao
@patch('app.routes.get_data')
def test_get_importacao(mock_get_data, valid_token):
    mock_get_data.return_value = {"data": ["importacao1", "importacao2"]}
    
    response = client.get("/importacao", headers={"Authorization": valid_token})
    
    mock_get_data.assert_called_once_with("importacao", None)
    
    assert response.status_code == 200
    assert "data" in response.json()
    assert isinstance(response.json()["data"], list)

# Testes para a rota /exportacao
@patch('app.routes.get_data')
def test_get_exportacao(mock_get_data, valid_token):
    mock_get_data.return_value = {"data": ["exportacao1", "exportacao2"]}
    
    response = client.get("/exportacao", headers={"Authorization": valid_token})
    
    mock_get_data.assert_called_once_with("exportacao", None)
    
    assert response.status_code == 200
    assert "data" in response.json()
    assert isinstance(response.json()["data"], list)

# Testes para as rotas CSV
@patch('app.routes.get_csv_data')
def test_producao_csv(mock_get_csv_data, valid_token):
    mock_get_csv_data.return_value = {"data": ["csv_producao1", "csv_producao2"]}
    
    response = client.get("/csv/producao", headers={"Authorization": valid_token})
    
    mock_get_csv_data.assert_called_once_with("producao")
    
    assert response.status_code == 200
    assert "data" in response.json()
    assert isinstance(response.json()["data"], list)

@patch('app.routes.get_csv_data')
def test_processamento_csv(mock_get_csv_data, valid_token):
    mock_get_csv_data.return_value = {"data": ["csv_processamento1", "csv_processamento2"]}
    
    response = client.get("/csv/processamento", headers={"Authorization": valid_token})
    
    mock_get_csv_data.assert_called_once_with("processamento")
    
    assert response.status_code == 200
    assert "data" in response.json()
    assert isinstance(response.json()["data"], list)

@patch('app.routes.get_csv_data')
def test_comercializacao_csv(mock_get_csv_data, valid_token):
    mock_get_csv_data.return_value = {"data": ["csv_comercializacao1", "csv_comercializacao2"]}
    
    response = client.get("/csv/comercializacao", headers={"Authorization": valid_token})
    
    mock_get_csv_data.assert_called_once_with("comercializacao")
    
    assert response.status_code == 200
    assert "data" in response.json()
    assert isinstance(response.json()["data"], list)

@patch('app.routes.get_csv_data')
def test_importacao_csv(mock_get_csv_data, valid_token):
    mock_get_csv_data.return_value = {"data": ["csv_importacao1", "csv_importacao2"]}
    
    response = client.get("/csv/importacao", headers={"Authorization": valid_token})
    
    mock_get_csv_data.assert_called_once_with("importacao")
    
    assert response.status_code == 200
    assert "data" in response.json()
    assert isinstance(response.json()["data"], list)

@patch('app.routes.get_csv_data')
def test_exportacao_csv(mock_get_csv_data, valid_token):
    mock_get_csv_data.return_value = {"data": ["csv_exportacao1", "csv_exportacao2"]}
    
    response = client.get("/csv/exportacao", headers={"Authorization": valid_token})
    
    mock_get_csv_data.assert_called_once_with("exportacao")
    
    assert response.status_code == 200
    assert "data" in response.json()
    assert isinstance(response.json()["data"], list)

# Testes de autenticação
def test_get_producao_invalid_token():
    response = client.get("/producao", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401

def test_get_producao_without_token():
    response = client.get("/producao")
    assert response.status_code == 401

def test_get_producao_with_invalid_year(valid_token):
    response = client.get("/producao?year=1969", headers={"Authorization": valid_token})
    assert response.status_code == 422
