import streamlit as st
import os
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from st_aggrid import AgGrid, GridOptionsBuilder
import plotly.express as px

# Funções auxiliares (mantidas do seu código)
def get_distinct_paises_from_csv(csv_path):
    try:
        df = pd.read_csv(csv_path)
        if 'pais' not in df.columns:
            raise ValueError("A coluna 'pais' não foi encontrada no arquivo CSV.")
        paises = df['pais'].dropna().unique().tolist()
        paises.sort()
        return paises
    except Exception as e:
        st.error(f"Erro ao obter os países distintos do arquivo CSV: {e}")
        return []

def get_historico_por_pais_from_csv(csv_path, pais):
    try:
        df = pd.read_csv(csv_path)
        df_pais = df[df['pais'] == pais]
        if df_pais.empty:
            return pd.DataFrame()
        df_pais['quantidade_litros'] = df_pais['quantidade_litros'].apply(lambda x: f"{x:,.2f}".replace(",", " "))
        df_pais['valor_usd'] = df_pais['valor_usd'].apply(lambda x: f"${x:,.2f}".replace(",", " "))
        df_pais = df_pais.sort_values(by=['ano', 'pais'], ascending=[False, True])
        return df_pais
    except Exception as e:
        st.error(f"Erro ao filtrar os dados do arquivo CSV: {e}")
        return pd.DataFrame()

def plot_distribution_by_region(csv_path):
    try:
        df = pd.read_csv(csv_path)
        if 'regiao' not in df.columns:
            raise ValueError("A coluna 'regiao' não foi encontrada no arquivo CSV.")
        region_counts = df['regiao'].value_counts()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=region_counts.index, y=region_counts.values, palette="viridis", ax=ax)
        ax.set_title("Distribuição de Países por Região", fontsize=16)
        ax.set_xlabel("Região", fontsize=14)
        ax.set_ylabel("Quantidade de Países", fontsize=14)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Erro ao plotar a distribuição por região: {e}")

def plot_world_map(csv_path):
    try:
        df = pd.read_csv(csv_path)
        required_columns = ['pais', 'quantidade_litros', 'valor_usd']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"A coluna '{col}' não foi encontrada no arquivo CSV.")
        
        # Traduzir os nomes dos países
        df["pais_ingles"] = df["pais"].map(country_translation)
        if df["pais_ingles"].isnull().any():
            st.warning("Atenção: Alguns países não foram traduzidos. Verifique o dicionário de tradução.")
            
            # Filtrar os países não traduzidos
            paises_nao_traduzidos = df[df["pais_ingles"].isnull()]["pais"].unique()
            
            # Exibir os países não traduzidos
            st.write("Países não traduzidos:")
            for pais in paises_nao_traduzidos:
                st.write(f"- {pais}")
        # Aplicar transformação logarítmica para destacar valores menores
        df["quantidade_litros_log"] = df["quantidade_litros"].apply(lambda x: max(x, 1)).apply(np.log)

        # Ajustar a escala de cores e o tamanho do mapa
        fig = px.choropleth(
            df,
            locations="pais_ingles",
            locationmode="country names",
            color="quantidade_litros_log",  # Usar a coluna transformada
            hover_name="pais",
            hover_data={"valor_usd": True, "quantidade_litros": True},
            color_continuous_scale=px.colors.sequential.Viridis,  # Escala de cores
            range_color=(df["quantidade_litros_log"].min(), df["quantidade_litros_log"].max()),  # Intervalo ajustado
            title="Distribuição de Exportação por País (Escala Logarítmica)",
            width=1200,  # Largura do mapa
            height=800   # Altura do mapa
        )
        
        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Erro ao gerar o mapa-múndi: {e}")

def plot_world_map_old(csv_path):
    try:
        df = pd.read_csv(csv_path)
        required_columns = ['pais', 'quantidade_litros', 'valor_usd']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"A coluna '{col}' não foi encontrada no arquivo CSV.")
        
        # Traduzir os nomes dos países
        df["pais_ingles"] = df["pais"].map(country_translation)
        if df["pais_ingles"].isnull().any():
            st.warning("Atenção: Alguns países não foram traduzidos. Verifique o dicionário de tradução.")
        
        # Ajustar a escala de cores e o tamanho do mapa
        fig = px.choropleth(
            df,
            locations="pais_ingles",
            locationmode="country names",
            color="quantidade_litros",
            hover_name="pais",
            hover_data={"valor_usd": True, "quantidade_litros": True},
            color_continuous_scale=px.colors.sequential.Viridis,  # Escala de cores
            range_color=(df["quantidade_litros"].min(), df["quantidade_litros"].max()),  # Intervalo de cores
            title="Distribuição de Exportação por País",
            width=1200,  # Largura do mapa
            height=800   # Altura do mapa
        )
        
        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Erro ao gerar o mapa-múndi: {e}")

def plot_scatter_avg_value_vs_quantity(csv_path):
    try:
        df = pd.read_csv(csv_path)
        if 'valor_medio_litro' not in df.columns or 'quantidade_litros' not in df.columns:
            raise ValueError("As colunas 'valor_medio_litro' e 'quantidade_litros' são necessárias no arquivo CSV.")
        
        fig = px.scatter(df, x='quantidade_litros', y='valor_medio_litro', 
                         title="Relação entre Valor Médio por Litro e Quantidade Exportada",
                         labels={'quantidade_litros': 'Quantidade de Litros', 'valor_medio_litro': 'Valor Médio por Litro (USD)'},
                         hover_data=['pais', 'ano'])
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Erro ao gerar o gráfico de dispersão: {e}")

def plot_linear_trend(csv_path):
     try:
         df = pd.read_csv(csv_path)
         if 'ano' not in df.columns or 'tendencia_quantidade' not in df.columns or 'tendencia_valor' not in df.columns:
             raise ValueError("As colunas 'ano', 'tendencia_quantidade' e 'tendencia_valor' são necessárias no arquivo CSV.")
         
         trend_data = df.groupby('ano')[['tendencia_quantidade', 'tendencia_valor']].mean().reset_index()
         fig = px.line(trend_data, x='ano', y=['tendencia_quantidade', 'tendencia_valor'], 
                       title="Tendência Linear de Quantidade e Valor Exportado",
                       labels={'ano': 'Ano', 'value': 'Tendência', 'variable': 'Métrica'})
         st.plotly_chart(fig)
     except Exception as e:
         st.error(f"Erro ao gerar o gráfico de tendência linear: {e}")

def plot_avg_value_per_liter(csv_path):
    try:
        df = pd.read_csv(csv_path)
        if 'ano' not in df.columns or 'valor_medio_litro' not in df.columns:
            raise ValueError("As colunas 'ano' e 'valor_medio_litro' são necessárias no arquivo CSV.")
        
        avg_value = df.groupby('ano')['valor_medio_litro'].mean().reset_index()
        fig = px.line(avg_value, x='ano', y='valor_medio_litro', 
                      title="Evolução do Valor Médio por Litro ao Longo do Tempo",
                      labels={'ano': 'Ano', 'valor_medio_litro': 'Valor Médio por Litro (USD)'})
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Erro ao gerar o gráfico de valor médio por litro: {e}")

def plot_time_series(csv_path):
    try:
        df = pd.read_csv(csv_path)
        if 'ano' not in df.columns or 'quantidade_litros' not in df.columns:
            raise ValueError("As colunas 'ano' e 'quantidade_litros' são necessárias no arquivo CSV.")
        time_series = df.groupby('ano')['quantidade_litros'].sum().reset_index()
        fig = px.line(
            time_series,
            x='ano',
            y='quantidade_litros',
            title="Tendência Temporal de Exportação",
            labels={'ano': 'Ano', 'quantidade_litros': 'Quantidade de Litros'}
        )
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Erro ao gerar o gráfico de tendência temporal: {e}")

def plot_country_share(csv_path):
    try:
        df = pd.read_csv(csv_path)
        if 'pais' not in df.columns or 'quantidade_litros' not in df.columns:
            raise ValueError("As colunas 'pais' e 'quantidade_litros' são necessárias no arquivo CSV.")
        country_share = df.groupby('pais')['quantidade_litros'].sum().reset_index()
        fig = px.pie(
            country_share,
            values='quantidade_litros',
            names='pais',
            title="Participação de Exportação por País",
            labels={'quantidade_litros': 'Quantidade de Litros', 'pais': 'País'}
        )
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Erro ao gerar o gráfico de participação por país: {e}")

def plot_correlation(csv_path):
    try:
        df = pd.read_csv(csv_path)
        if 'quantidade_litros' not in df.columns or 'valor_usd' not in df.columns:
            raise ValueError("As colunas 'quantidade_litros' e 'valor_usd' são necessárias no arquivo CSV.")
        fig = px.scatter(
            df,
            x='quantidade_litros',
            y='valor_usd',
            title="Correlação entre Valor e Quantidade Exportada",
            labels={'quantidade_litros': 'Quantidade de Litros', 'valor_usd': 'Valor (USD)'},
            hover_data=['pais', 'ano']
        )
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Erro ao gerar o gráfico de correlação: {e}")

def plot_exports_by_region(csv_path):
    try:
        df = pd.read_csv(csv_path)
        if 'regiao' not in df.columns or 'quantidade_litros' not in df.columns:
            raise ValueError("As colunas 'regiao' e 'quantidade_litros' são necessárias no arquivo CSV.")
        region_exports = df.groupby('regiao')['quantidade_litros'].sum().reset_index()
        fig = px.bar(
            region_exports,
            x='regiao',
            y='quantidade_litros',
            title="Exportações por Região",
            labels={'regiao': 'Região', 'quantidade_litros': 'Quantidade de Litros'}
        )
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Erro ao gerar o gráfico de exportações por região: {e}")
def plot_annual_variation(csv_path):
    try:
        df = pd.read_csv(csv_path)
        if 'ano' not in df.columns or 'quantidade_litros_var' not in df.columns or 'valor_usd_var' not in df.columns:
            raise ValueError("As colunas 'ano', 'quantidade_litros_var' e 'valor_usd_var' são necessárias no arquivo CSV.")
        
        variation = df.groupby('ano')[['quantidade_litros_var', 'valor_usd_var']].sum().reset_index()
        fig = px.bar(variation, x='ano', y=['quantidade_litros_var', 'valor_usd_var'], 
                     title="Variação Anual de Quantidade e Valor Exportado",
                     labels={'ano': 'Ano', 'value': 'Variação', 'variable': 'Métrica'},
                     barmode='group')
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Erro ao gerar o gráfico de variação anual: {e}")

# Dicionário para traduzir os nomes dos países
country_translation = {
    "Alemanha, República Democrática": "Germany",
    "Angola": "Angola",
    "Antígua e Barbuda": "Antigua and Barbuda",
    "Argentina": "Argentina",
    "Austrália": "Australia",
    "Áustria": "Austria",
    "Bahamas": "Bahamas",
    "Bangladesh": "Bangladesh",
    "Barbados": "Barbados",
    "Barein": "Bahrain",
    "Bélgica": "Belgium",
    "Bolívia": "Bolivia",
    "Brasil": "Brazil",
    "Bulgária": "Bulgaria",
    "Canadá": "Canada",
    "Cayman, Ilhas": "Cayman Islands",
    "Chile": "Chile",
    "China": "China",
    "Chipre": "Cyprus",
    "Cocos (Keeling), Ilhas": "Cocos (Keeling) Islands",
    "Colômbia": "Colombia",
    "Coreia, Republica Sul": "South Korea",
    "Croácia": "Croatia",
    "Cuba": "Cuba",
    "Curaçao": "Curaçao",
    "Dinamarca": "Denmark",
    "Dominica": "Dominica",
    "Emirados Arabes Unidos": "United Arab Emirates",
    "Equador": "Ecuador",
    "Estados Unidos": "United States",
    "Filipinas": "Philippines",
    "França": "France",
    "Gana": "Ghana",
    "Granada": "Grenada",
    "Grécia": "Greece",
    "Guatemala": "Guatemala",
    "Guiana": "Guyana",
    "Guiana Francesa": "French Guiana",
    "Haiti": "Haiti",
    "Hong Kong": "Hong Kong",
    "Ilha de Man": "Isle of Man",
    "India": "India",
    "Irã": "Iran",
    "Itália": "Italy",
    "Japão": "Japan",
    "Libéria": "Liberia",
    "Luxemburgo": "Luxembourg",
    "Malta": "Malta",
    "Marshall, Ilhas": "Marshall Islands",
    "México": "Mexico",
    "Moçambique": "Mozambique",
    "Nigéria": "Nigeria",
    "Noruega": "Norway",
    "Nova Zelândia": "New Zealand",
    "Omã": "Oman",
    "Países Baixos": "Netherlands",
    "Panamá": "Panama",
    "Paraguai": "Paraguay",
    "Portugal": "Portugal",
    "Quênia": "Kenya",
    "Reino Unido": "United Kingdom",
    "Rússia": "Russia",
    "São Vicente e Granadinas": "Saint Vincent and the Grenadines",
    "Serra Leoa": "Sierra Leone",
    "Singapura": "Singapore",
    "Suécia": "Sweden",
    "Suíça": "Switzerland",
    "Suriname": "Suriname",
    "Tailândia": "Thailand",
    "Taiwan (Formosa)": "Taiwan",
    "Tcheca, República": "Czech Republic",
    "Togo": "Togo",
    "Turquia": "Turkey",
    "Uruguai": "Uruguay",
    "Venezuela": "Venezuela",
    "Vietnã": "Vietnam",
    "Cingapura": "Singapore",
    "Estônia": "Estonia",
    "Finlândia": "Finland",
    "Polônia": "Poland",
    "Total": "Total",  # Não é um país, mas mantido como está
    "Antilhas Holandesas": "Netherlands Antilles",
    "Aruba": "Aruba",
    "Afeganistão": "Afghanistan",
    "Cabo Verde": "Cape Verde",
    "Catar": "Qatar",
    "Hungria": "Hungary",
    "Irlanda": "Ireland",
    "Mauritânia": "Mauritania",
    "Montenegro": "Montenegro",
    "Nova Caledônia": "New Caledonia",
    "Peru": "Peru",
    "Suazilândia": "Eswatini",  # Nome atualizado
    "Guine Equatorial": "Equatorial Guinea",
    "Trinidade Tobago": "Trinidad and Tobago",
    "África do Sul": "South Africa",
    "Belice": "Belize",
    "Benin": "Benin",
    "Espanha": "Spain",
    "Camarões": "Cameroon",
    "Arábia Saudita": "Saudi Arabia",
    "Bermudas": "Bermuda",
    "Congo": "Congo",
    "Indonésia": "Indonesia",
    "Letônia": "Latvia",
    "Macau": "Macau",
    "Malavi": "Malawi",
    "Martinica": "Martinique",
    "Palau": "Palau",
    "Pitcairn": "Pitcairn Islands",
    "São Cristóvão e Névis": "Saint Kitts and Nevis",
    "Toquelau": "Tokelau",
    "Bósnia-Herzegovina": "Bosnia and Herzegovina",
    "Comores": "Comoros",
    "Gibraltar": "Gibraltar",
    "Índia": "India",
    "Jordânia": "Jordan",
    "Tuvalu": "Tuvalu",
    "Vanuatu": "Vanuatu",
    "Malásia": "Malaysia",
    "São Tomé e Príncipe": "Sao Tome and Principe",
    "Guine Bissau": "Guinea-Bissau"
}

# Configuração inicial
csv_path = os.path.join(os.getcwd(), 'ml-model', 'training', 'dados_para_treinamento.csv')
model_path = os.path.join(os.getcwd(), 'ml-model', 'production', 'modelo_exportacao.pkl')
model = joblib.load(model_path)
paises_disponiveis = get_distinct_paises_from_csv(csv_path)

# Layout da aplicação
st.set_page_config(page_title="Previsão de Exportação de Vinhos", layout="wide")
st.sidebar.title("Menu de Navegação")
menu = st.sidebar.radio("Selecione uma opção:", ["Mapa-Global", "Gráficos", "Histórico", "Previsão"])

# Seção: Mapa-Global
if menu == "Mapa-Global":
    st.title("Mapa-Global de Exportação")
    st.write("Este mapa mostra a distribuição de exportação por país com base nos dados fornecidos.")
    plot_world_map(csv_path)

# Seção: Gráficos
elif menu == "Gráficos":
    st.title("Gráficos de Análise")
    grafico_opcao = st.selectbox("Selecione o gráfico:", [
        "Tendência Temporal de Exportação",
        "Correlação entre Valor e Quantidade Exportada",
        "Exportações por Região"
    ])
    
    st.title("Gráficos de Análise")
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Tendência Temporal")
        plot_time_series(csv_path)

    with col2:
        st.subheader("Exportações por Região")
        plot_exports_by_region(csv_path)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Variação Anual (Quantidade e Valor)")
        plot_annual_variation(csv_path)
    with col4:
        st.subheader("Dispersão (Valor Médio por Litro vs. Quantidade)")
        plot_scatter_avg_value_vs_quantity(csv_path)

# Seção: Histórico
elif menu == "Histórico":
    st.title("Histórico de Exportação")
    novo_pais = st.selectbox("Selecione um país para visualizar o histórico:", paises_disponiveis)
    if novo_pais:
        historico_df = get_historico_por_pais_from_csv(csv_path, novo_pais)
        if not historico_df.empty:
            st.subheader(f"Histórico de Exportação para {novo_pais}")
            AgGrid(historico_df)
        else:
            st.write("Nenhum histórico encontrado para este país.")

# Seção: Previsão
elif menu == "Previsão":
    st.title("Previsão de Exportação")
    novo_pais = st.selectbox("Selecione um país para previsão:", paises_disponiveis)
    if st.button("Prever"):
        try:
            new_data = pd.DataFrame({'pais': [novo_pais]})
            predicao = model.predict(new_data)
            quantidade_prevista = max(predicao[0][0], 0)
            valor_previsto = max(predicao[0][1], 0)
            st.subheader("Resultados da Previsão:")
            st.write(f"**País:** {novo_pais}")
            st.write(f"**Quantidade de Litros Prevista:** {quantidade_prevista:,.2f}")
            st.write(f"**Valor em USD Previsto:** ${valor_previsto:,.2f}")
        except Exception as e:
            st.error(f"Erro ao realizar a previsão: {e}")