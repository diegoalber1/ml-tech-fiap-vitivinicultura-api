import requests
import csv
import io
import json
import logging
from bs4 import BeautifulSoup

# Configuração de logging
logging.basicConfig(level=logging.INFO)

# Caminho do arquivo de configuração
CONFIG_PATH = 'data/config.json'

# Carrega a configuração a partir de um arquivo JSON
def load_config(config_path=CONFIG_PATH):
    with open(config_path, 'r') as f:
        return json.load(f)

# Carrega as URLs de configuração
config = load_config()
BASE_URL = config["base_url"]
SECTIONS = config["sections"]
CSV_URLS = config["csv_urls"]

def get_data(section, year=None):
    """
    Obtém dados de uma seção específica.

    :param section: Seção a ser consultada.
    :param year: Ano opcional para filtrar os dados.
    :return: Dados da seção ou erro.
    """
    if section not in SECTIONS:
        return {"error": "Seção inválida"}

    url = f"{BASE_URL}{SECTIONS[section]}"
    if year:
        url += f"&ano={year}"

    logging.info(f"services->get_data()->{url}")

    try:
        response = requests.get(url)
        response.raise_for_status()  # Lança um erro para códigos de status 4xx/5xx
    except requests.RequestException as e:
        logging.error(f"Erro ao acessar os dados: {e}")
        return {"error": "Não foi possível acessar os dados"}

    soup = BeautifulSoup(response.content, "html.parser")
    return parse_data(soup)

def parse_data(soup):
    """
    Faz o parsing dos dados da tabela.

    :param soup: Objeto BeautifulSoup com o conteúdo da página.
    :return: Dados da tabela ou erro.
    """
    table = soup.find('table', class_='tb_base tb_dados')
    if not table:
        return {"error": "Tabela não encontrada"}

    headers = [header.text.strip() for header in table.find_all('th')]
    rows = []

    for row in table.find_all('tr'):
        cols = row.find_all('td')
        if cols:
            rows.append([col.text.strip() for col in cols])

    return {"headers": headers, "rows": rows}

def get_csv_data(section):
    """
    Obtém dados de um arquivo CSV de uma seção específica.

    :param section: Seção a ser consultada.
    :return: Dados do CSV ou erro.
    """
    if section not in CSV_URLS:
        return {"error": "Seção inválida"}

    csv_url = CSV_URLS[section]
    logging.info(f"services->get_csv_data()->{csv_url}")

    try:
        response = requests.get(csv_url)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Erro ao acessar o arquivo CSV: {e}")
        return {"error": "Não foi possível acessar o arquivo CSV"}

    csv_content = response.content.decode('utf-8')
    csv_reader = csv.reader(io.StringIO(csv_content))
    csv_data = []
    headers = next(csv_reader)

    for row in csv_reader:
        csv_data.append(dict(zip(headers, row)))

    return csv_data
