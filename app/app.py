import streamlit as st
import os
import pandas as pd
import joblib
from st_aggrid import AgGrid, GridOptionsBuilder


def get_distinct_paises_from_csv(csv_path):
    """Obtém os valores distintos da coluna 'pais' no arquivo CSV."""
    try:
        # Ler o arquivo CSV
        df = pd.read_csv(csv_path)
        
        # Verificar se a coluna 'pais' existe
        if 'pais' not in df.columns:
            raise ValueError("A coluna 'pais' não foi encontrada no arquivo CSV.")
        
        # Obter os valores únicos da coluna 'pais'
        paises = df['pais'].dropna().unique().tolist()
        
        # Ordenar os países em ordem alfabética
        paises.sort()
        
        return paises
    except Exception as e:
        print(f"Erro ao obter os países distintos do arquivo CSV: {e}")
        return []



def get_historico_por_pais_from_csv(csv_path, pais):
    """Filtra o histórico de exportação por país a partir do arquivo CSV."""
    try:
        df = pd.read_csv(csv_path)
        df_pais = df[df['pais'] == pais]
        if df_pais.empty:
            return pd.DataFrame()
        # Formatar os campos
        df_pais['quantidade_litros'] = df_pais['quantidade_litros'].apply(lambda x: f"{x:,.2f}".replace(",", " "))
        df_pais['valor_usd'] = df_pais['valor_usd'].apply(lambda x: f"${x:,.2f}".replace(",", " "))
        # Ordenar o DataFrame por ano em ordem decrescente
        # Ordenar o DataFrame por ano (decrescente) e país (alfabética)
        df_pais = df_pais.sort_values(by=['ano', 'pais'], ascending=[False, True])
        return df_pais
    except Exception as e:
        st.error(f"Erro ao filtrar os dados do arquivo CSV: {e}")
        return pd.DataFrame()


# Obter o diretório atual do notebook
notebook_dir = os.getcwd()

# Subir dois níveis na hierarquia de diretórios
parent_dir_two_levels_up = os.path.abspath(os.path.join(notebook_dir, os.pardir, os.pardir))


csv_dir = os.path.join(notebook_dir, 'ml-model', 'training')
csv_path = os.path.join(csv_dir, 'dados_para_treinamento.csv')

open_dir = os.path.join(notebook_dir, 'ml-model', 'production')
# Caminho completo para os modelos
model_path = os.path.join(open_dir, 'modelo_exportacao.pkl')
encoder_path = os.path.join(open_dir, 'encoder_exportacao.pkl')

# Carregar o modelo
model = joblib.load(model_path)


# Obter os valores distintos da tabela exportacao
paises_disponiveis = get_distinct_paises_from_csv(csv_path)

# Interface do Streamlit
st.title("Previsão de Exportação de Vinhos")
st.write("Insira os dados abaixo para realizar a previsão:")

# Inputs do usuário
# novo_ano = st.number_input("Ano", min_value=2024, max_value=2100, value=2025, step=1)
novo_pais = st.selectbox("País", paises_disponiveis)

#Mostrar o histórico ao selecionar o país
if novo_pais:
    st.subheader(f"Histórico de Exportação para {novo_pais}")
    #historico_df = get_historico_por_pais(novo_pais)
    historico_df = get_historico_por_pais_from_csv(csv_path, novo_pais)
    if not historico_df.empty:
        # Configurar a grid para exibir os dados formatados
        gb = GridOptionsBuilder.from_dataframe(historico_df)
        gb.configure_column("quantidade_litros", type=["numericColumn"], valueFormatter="x.toLocaleString('en-US')")
        gb.configure_column("valor_usd", type=["numericColumn"], valueFormatter="x.toLocaleString('en-US', {style: 'currency', currency: 'USD'})")
        grid_options = gb.build()
        AgGrid(historico_df, gridOptions=grid_options)
    else:
        st.write("Nenhum histórico encontrado para este país.")

# Botão para realizar a previsão
if st.button("Prever"):
    try:

        # Fazer previsões 
        new_data = pd.DataFrame({
            'pais': [novo_pais]
        })

        # Fazer a previsão
        predicao = model.predict(new_data)

        # Garantir que valores negativos sejam exibidos como zero
        quantidade_prevista = predicao[0][0]  # Quantidade de Litros
        valor_previsto = predicao[0][1]  # Valor em USD

        # Garantir que valores negativos sejam exibidos como zero
        quantidade_prevista = max(quantidade_prevista, 0)
        valor_previsto = max(valor_previsto, 0)
        # Exibir os resultados formatados
        st.subheader("Resultados da Previsão:")
        st.write(f"**País:** {novo_pais}")
        st.write(f"**Quantidade de Litros Prevista:** {quantidade_prevista:,.2f}".replace(",", " "))
        st.write(f"**Valor em USD Previsto:** ${valor_previsto:,.2f}".replace(",", " "))
    except Exception as e:
        st.error(f"Erro ao realizar a previsão: {e}")