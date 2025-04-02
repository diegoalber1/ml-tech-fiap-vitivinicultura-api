import requests
import csv
import io
import json
import logging
from bs4 import BeautifulSoup
from app.database import get_db_connection
import logging
import pandas as pd
import joblib
import os

# Configuração de logging
logging.basicConfig(level=logging.INFO)

# Caminho do arquivo de configuração
CONFIG_PATH = 'data/config.json'

# Caminhos para os arquivos do modelo e encoder
MODEL_PATH = os.path.join("ml-model", "production", "modelo_exportacao.pkl")
ENCODER_PATH = os.path.join("ml-model", "production", "encoder_exportacao.pkl")

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



def save_producao_data(data, year):
    """
    Salva os dados de produção no banco de dados.
    :param data: Dados retornados pela função get_data.
    :param year: Ano dos dados a serem salvos.
    """
    if "error" in data:
        logging.error(f"Erro nos dados: {data['error']}")
        return {"status": "error", "message": data["error"]}

    headers = data["headers"]
    rows = data["rows"]
    logging.info(f"Headers retornados: {headers}")

    # Mapeamento de colunas para os campos do banco de dados
    column_mapping = {
        "Produto": "produto",
        "Quantidade (L.)": "quantidade_litros",
    }

    # Verifica se os headers correspondem às colunas esperadas
    db_columns = [column_mapping.get(header, None) for header in headers]
    if None in db_columns:
        logging.error("Os headers não correspondem às colunas esperadas.")
        return {"status": "error", "message": "Headers inválidos."}

    conn = get_db_connection()
    cursor = conn.cursor()

    # Query de inserção
    query = """
        INSERT INTO producao (ano, produto, quantidade_litros)
        VALUES (%s, %s, %s)
        ON CONFLICT (ano, produto) DO UPDATE
        SET quantidade_litros = EXCLUDED.quantidade_litros;
    """

    try:
        for row in rows:
            # Mapeia os valores para as colunas do banco
            values = [row[headers.index(header)] for header in headers]

            # Remove os pontos do valor de "Quantidade (L.)"
            if "Quantidade (L.)" in headers:
                quantidade_index = headers.index("Quantidade (L.)")
                values[quantidade_index] = values[quantidade_index].replace('.', '') if values[quantidade_index] != '-' else None

            # Adiciona o ano aos valores
            values.insert(0, year)

            # Converte o valor de quantidade para inteiro, se não for nulo
            if values[2] is not None:
                values[2] = int(values[2])

            cursor.execute(query, values)

        conn.commit()
        logging.info("Dados de produção salvos com sucesso.")
        return {"status": "success", "message": "Dados salvos com sucesso."}
    except Exception as e:
        conn.rollback()
        logging.error(f"Erro ao salvar os dados: {e}")
        return {"status": "error", "message": "Erro ao salvar os dados."}
    finally:
        cursor.close()
        conn.close() 

def fetch_and_save_producao(year):
    """
    Obtém os dados de produção e os salva no banco de dados.

    :param year: Ano para filtrar os dados.
    :return: Mensagem de sucesso ou erro.
    """
    data = get_data("producao", year)
    saved_data = save_producao_data(data, year)
    return data


def save_exportacao_data(data, year):
    """ Salva os dados de exportação no banco de dados.
    :param data: Dados retornados pela função get_data.
    :param year: Ano dos dados a serem salvos.
    """
    if "error" in data:
        logging.error(f"Erro nos dados: {data['error']}")
        return {"status": "error", "message": data["error"]}

    headers = data["headers"]
    rows = data["rows"]
    logging.info(f"Headers retornados: {headers}")

    # Mapeamento de colunas para os campos do banco de dados
    column_mapping = {
        "Países": "pais",
        "Quantidade (Kg)": "quantidade_litros",
        "Valor (US$)": "valor_usd",
    }

    # Verifica se os headers correspondem às colunas esperadas
    db_columns = [column_mapping.get(header, None) for header in headers]
    if None in db_columns:
        logging.error("Os headers não correspondem às colunas esperadas.")
        return {"status": "error", "message": "Headers inválidos."}

    conn = get_db_connection()
    cursor = conn.cursor()

    # Query de inserção
    query = """
        INSERT INTO exportacao (ano, pais, quantidade_litros, valor_usd)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (ano, pais) DO UPDATE
        SET quantidade_litros = EXCLUDED.quantidade_litros,
            valor_usd = EXCLUDED.valor_usd;
    """

    try:
        for row in rows:
            # Mapeia os valores para as colunas do banco
            values = [row[headers.index(header)] for header in headers]

            # Remove os pontos e vírgulas dos valores numéricos e trata valores inválidos
            if "Quantidade (Kg)" in headers:
                quantidade_index = headers.index("Quantidade (Kg)")
                values[quantidade_index] = (
                    values[quantidade_index].replace('.', '').replace(',', '')
                    if values[quantidade_index] != '-' else None
                )

            if "Valor (US$)" in headers:
                valor_index = headers.index("Valor (US$)")
                values[valor_index] = (
                    values[valor_index].replace('.', '').replace(',', '')
                    if values[valor_index] != '-' else None
                )

            # Adiciona o ano aos valores
            values.insert(0, year)

            # Converte os valores para os tipos corretos, se não forem nulos
            if values[2] is not None:  # Quantidade (Kg)
                values[2] = int(values[2])
            if values[3] is not None:  # Valor (US$)
                values[3] = float(values[3])

            # Executa a query
            cursor.execute(query, values)

        conn.commit()
        logging.info("Dados de exportação salvos com sucesso.")
        return {"status": "success", "message": "Dados salvos com sucesso."}

    except Exception as e:
        conn.rollback()
        logging.error(f"Erro ao salvar os dados: {e}")
        return {"status": "error", "message": "Erro ao salvar os dados."}

    finally:
        cursor.close()
        conn.close()

def fetch_and_save_exportacao(year):
    """
    Obtém os dados de exportacao e os salva no banco de dados.

    :param year: Ano para filtrar os dados.
    :return: Mensagem de sucesso ou erro.
    """
    data = get_data("exportacao", year)
    saved_data = save_exportacao_data(data, year)
    return data


def exportacao_predict_wrapper(country: str):
    """
    Função para prever a quantidade de litros de exportação com base no país informado.

    Args:
        country (str): País para a previsão (ex: "Brasil").

    Returns:
        dict: Resultado da previsão contendo o ano, país, quantidade prevista e valor previsto.
    """
    try:
        # Carregar o modelo e o encoder
        model = joblib.load(MODEL_PATH)

        input_data = pd.DataFrame({'pais': [country]})

        # Fazer a previsão
        predicao = model.predict(input_data)
        quantidade_prevista = max(predicao[0][0], 0)
        valor_previsto = max(predicao[0][1], 0)

        # Retornar os resultados formatados
        return {
            "pais": country,
            "quantidade_prevista": round(quantidade_prevista, 2),
            "valor_previsto": round(valor_previsto, 2)
        }

    except Exception as e:
        raise RuntimeError(f"Erro ao realizar a previsão: {e}")
    
def get_jwt_token():
    """
    Obtém o token JWT para autenticação.
    """
    url = f"{BASE_URL}/token"
    payload = {
        "username": os.getenv("USERNAME"),
        "password": os.getenv("PASSWORD")
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Erro ao obter o token: {response.status_code} - {response.text}")

def call_exportacao_predict(year, country):
    """
    Faz a chamada ao endpoint /exportacao/predict.
    """
    token = get_jwt_token()
    url = f"{os.getenv("BASE_URL_APP")}/exportacao/predict"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "year": year,
        "country": country
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro ao chamar o endpoint: {response.status_code} - {response.text}")
