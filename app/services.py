import requests
import csv
import io
import json
from bs4 import BeautifulSoup

# Carrega a configuração a partir de um arquivo JSON
def load_config(config_path='data/config.json'):
    with open(config_path, 'r') as f:
        return json.load(f)

# Carrega as URLs de configuração
config = load_config()

BASE_URL = config["base_url"]
SECTIONS = config["sections"]
CSV_URLS = config["csv_urls"]

def get_data(section, year=None):
    # Verifica se a seção existe no mapeamento
    if section not in SECTIONS:
        return {"error": "Seção inválida"}

    # Constrói a URL completa para a seção
    url = f"{BASE_URL}{SECTIONS[section]}"

    # Adiciona o ano como parâmetro de consulta, se fornecido
    if year:
        url += f"&ano={year}"

    print(f"services->get_data()->{url}")

    # Faz a requisição HTTP
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        # Faz o parsing dos dados da tabela
        data = parse_data(soup)
        return data
    else:
        return {"error": "Não foi possível acessar os dados"}

def parse_data(soup):
    # Encontra a tabela com a classe 'tb_base tb_dados'
    table = soup.find('table', class_='tb_base tb_dados')

    # Verifica se a tabela foi encontrada
    if not table:
        return {"error": "Tabela não encontrada"}

    # Extrai os cabeçalhos da tabela
    headers = [header.text.strip() for header in table.find_all('th')]

    # Extrai as linhas de dados
    rows = []
    for row in table.find_all('tr'):
        cols = row.find_all('td')
        if cols:
            rows.append([col.text.strip() for col in cols])

    # Retorna os dados em formato de dicionário
    return {"headers": headers, "rows": rows}

def get_csv_data(section):
    # Verifica se a seção existe no mapeamento de CSVs
    if section not in CSV_URLS:
        return {"error": "Seção inválida"}

    # Faz o download do arquivo CSV
    csv_url = CSV_URLS[section]
    print(f"services->get_csv_data()->{csv_url}")
    response = requests.get(csv_url)
    if response.status_code == 200:
        # Lê o conteúdo do CSV
        csv_content = response.content.decode('utf-8')
        csv_reader = csv.reader(io.StringIO(csv_content))

        # Converte o CSV para uma lista de dicionários
        csv_data = []
        headers = next(csv_reader)  # Primeira linha são os cabeçalhos
        for row in csv_reader:
            csv_data.append(dict(zip(headers, row)))

        return csv_data
    else:
        return {"error": "Não foi possível acessar o arquivo CSV"}
