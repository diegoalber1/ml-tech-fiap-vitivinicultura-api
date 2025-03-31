import streamlit as st
import os
import pandas as pd
import psycopg2
from psycopg2 import sql
import joblib
from st_aggrid import AgGrid, GridOptionsBuilder

# Configuração da conexão com o banco de dados PostgreSQL
DB_CONFIG = {
    "dbname": "vitivinicultura_db",
    "user": "postgres",
    "password": "102030",
    "host": "localhost",
    "port": 5432
}

def get_distinct_paises():
    """Consulta os valores distintos da coluna 'Países' na tabela exportacao."""
    try:
        # Conectar ao banco de dados
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        # Query para obter os valores distintos
        query = sql.SQL("SELECT DISTINCT pais FROM exportacao WHERE pais IS NOT NULL ORDER BY pais;")
        cursor.execute(query)
        # Obter os resultados
        paises = [row[0] for row in cursor.fetchall()]
        # Fechar a conexão
        cursor.close()
        conn.close()
        return paises
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return []

def get_historico_por_pais(pais):
    """Consulta o histórico de quantidade e valor por ano para o país selecionado."""
    try:
        # Conectar ao banco de dados
        conn = psycopg2.connect(**DB_CONFIG)
        # Criar a consulta como uma string
        query = """
        SELECT 
            ano, 
            COALESCE(quantidade_litros, 0) AS "Quantidade", 
            COALESCE(valor_usd, 0) AS "Valor (US$)"
        FROM exportacao 
        WHERE pais = %s 
        ORDER BY ano;
        """
        # Executar a consulta e carregar os dados em um DataFrame
        df = pd.read_sql_query(query, conn, params=(pais,))
        conn.close()
        # Formatar os campos
        df["Quantidade"] = df["Quantidade"].apply(lambda x: f"{x:,.2f}".replace(",", " "))
        df["Valor (US$)"] = df["Valor (US$)"].apply(lambda x: f"${x:,.2f}".replace(",", " "))
        return df
    except Exception as e:
        st.error(f"Erro ao consultar o histórico: {e}")
        return pd.DataFrame()

# Obter os valores distintos da tabela exportacao
paises_disponiveis = get_distinct_paises()


# Obter o diretório atual do notebook
notebook_dir = os.getcwd()


# Subir dois níveis na hierarquia de diretórios
parent_dir_two_levels_up = os.path.abspath(os.path.join(notebook_dir, os.pardir, os.pardir))


# Obter o diretório atual do notebook
notebook_dir = os.getcwd()
print(notebook_dir)

open_dir = os.path.join(notebook_dir, 'ml-model', 'production')
# Caminho completo para os modelos
model_path = os.path.join(open_dir, 'modelo_exportacao.pkl')
encoder_path = os.path.join(open_dir, 'encoder_exportacao.pkl')

# Carregar o modelo e o encoder
model = joblib.load(model_path)
encoder = joblib.load(encoder_path)


# Interface do Streamlit
st.title("Previsão de Exportação de Vinhos")
st.write("Insira os dados abaixo para realizar a previsão:")

# Inputs do usuário
novo_ano = st.number_input("Ano", min_value=2024, max_value=2100, value=2025, step=1)
novo_pais = st.selectbox("País", paises_disponiveis)

# Mostrar o histórico ao selecionar o país
# if novo_pais:
#     st.subheader(f"Histórico de Exportação para {novo_pais}")
#     historico_df = get_historico_por_pais(novo_pais)
#     if not historico_df.empty:
#         # Configurar a grid para exibir os dados formatados
#         gb = GridOptionsBuilder.from_dataframe(historico_df)
#         gb.configure_column("Quantidade", type=["numericColumn"], valueFormatter="x.toLocaleString('en-US')")
#         gb.configure_column("Valor (US$)", type=["numericColumn"], valueFormatter="x.toLocaleString('en-US', {style: 'currency', currency: 'USD'})")
#         grid_options = gb.build()
#         AgGrid(historico_df, gridOptions=grid_options)
#     else:
#         st.write("Nenhum histórico encontrado para este país.")

# Botão para realizar a previsão
if st.button("Prever"):
    try:
        # Codificar o país
        novo_pais_encoded = encoder.transform([[novo_pais]])
        # Criar o DataFrame de entrada
        entrada = pd.DataFrame(
            [list([novo_ano]) + list(novo_pais_encoded[0])],
            columns=['ano'] + encoder.get_feature_names_out(['pais']).tolist()
        )
        # Fazer a previsão
        quantidade_prevista, valor_previsto = model.predict(entrada)[0]
        # Garantir que valores negativos sejam exibidos como zero
        quantidade_prevista = max(quantidade_prevista, 0)
        valor_previsto = max(valor_previsto, 0)
        # Exibir os resultados formatados
        st.subheader("Resultados da Previsão:")
        st.write(f"**Ano:** {novo_ano}")
        st.write(f"**País:** {novo_pais}")
        st.write(f"**Quantidade de Litros Prevista:** {quantidade_prevista:,.2f}".replace(",", " "))
        st.write(f"**Valor em USD Previsto:** ${valor_previsto:,.2f}".replace(",", " "))
    except Exception as e:
        st.error(f"Erro ao realizar a previsão: {e}")