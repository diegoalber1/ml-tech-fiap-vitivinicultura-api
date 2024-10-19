import pytest
import requests
import requests_mock
from bs4 import BeautifulSoup
from app.services import get_data, parse_data, get_csv_data

# Teste para a função get_data
def test_get_data_success(requests_mock):
    # Mock da resposta HTML
    html_content = """
    <html>
        <body>
            <table class="tb_base tb_dados">
                <tr><th>Header1</th><th>Header2</th></tr>
                <tr><td>Data1</td><td>Data2</td></tr>
            </table>
        </body>
    </html>
    """
    # URL mockada
    url = "https://web.archive.org/web/20200217141254/http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02"
    requests_mock.get(url, text=html_content)

    # Chama a função
    result = get_data("producao")

    # Verifica se os dados retornados estão corretos
    assert result == {
        "headers": ["Header1", "Header2"],
        "rows": [["Data1", "Data2"]]
    }

def test_get_data_invalid_section():
    # Testa uma seção inválida
    result = get_data("invalid_section")
    assert result == {"error": "Seção inválida"}

def test_get_data_no_table(requests_mock):
    # Mock de uma página sem tabela
    html_content = "<html><body><p>No table here</p></body></html>"
    url = "https://web.archive.org/web/20200217141254/http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02"
    requests_mock.get(url, text=html_content)

    # Chama a função
    result = get_data("producao")

    # Verifica se o erro é retornado corretamente
    assert result == {"error": "Tabela não encontrada"}

# Teste para a função parse_data
def test_parse_data():
    # Mock de um objeto BeautifulSoup
    html_content = """
    <html>
        <body>
            <table class="tb_base tb_dados">
                <tr><th>Header1</th><th>Header2</th></tr>
                <tr><td>Data1</td><td>Data2</td></tr>
            </table>
        </body>
    </html>
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # Chama a função
    result = parse_data(soup)

    # Verifica se os dados retornados estão corretos
    assert result == {
        "headers": ["Header1", "Header2"],
        "rows": [["Data1", "Data2"]]
    }

def test_parse_data_no_table():
    # Mock de um objeto BeautifulSoup sem tabela
    html_content = "<html><body><p>No table here</p></body></html>"
    soup = BeautifulSoup(html_content, "html.parser")

    # Chama a função
    result = parse_data(soup)

    # Verifica se o erro é retornado corretamente
    assert result == {"error": "Tabela não encontrada"}

# Teste para a função get_csv_data
def test_get_csv_data_success(requests_mock):
    # Mock do conteúdo CSV
    csv_content = "Header1,Header2\nData1,Data2\n"
    csv_url = "https://web.archive.org/web/20201203223441/http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv"
    requests_mock.get(csv_url, text=csv_content)

    # Chama a função
    result = get_csv_data("producao")

    # Verifica se os dados retornados estão corretos
    assert result == [
        {"Header1": "Data1", "Header2": "Data2"}
    ]

def test_get_csv_data_invalid_section():
    # Testa uma seção inválida
    result = get_csv_data("invalid_section")
    assert result == {"error": "Seção inválida"}

def test_get_csv_data_error(requests_mock):
    # Mock de uma falha na requisição
    csv_url = "https://web.archive.org/web/20201203223441/http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv"
    requests_mock.get(csv_url, status_code=404)

    # Chama a função
    result = get_csv_data("producao")

    # Verifica se o erro é retornado corretamente
    assert result == {"error": "Não foi possível acessar o arquivo CSV"}