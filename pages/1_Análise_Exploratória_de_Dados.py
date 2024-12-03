# pages/2_Análise_Exploratória_de_Dados.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Análise Exploratória de Dados')

st.write("""
Nesta seção, examinamos os dados históricos do preço do petróleo Brent e da cotação do dólar. A análise exploratória nos ajuda a entender padrões, tendências e possíveis outliers nos dados.
""")

# Leitura dos dados
df_preco_petroleo = pd.read_csv('tabela_dxgvTable.csv', encoding="windows-1252", sep=";")
df_preco_petroleo = df_preco_petroleo.dropna()
df_preco_petroleo['DATA'] = pd.to_datetime(df_preco_petroleo['DATA'], dayfirst=True)
df_preco_petroleo["Preço - petróleo bruto - Brent (FOB)"] = df_preco_petroleo["Preço - petróleo bruto - Brent (FOB)"].str.replace(",", ".").astype("float")

df_cotacao_dolar = pd.read_csv('tabela_dxgvTable_dolar.csv', encoding="windows-1252", sep=";")
df_cotacao_dolar['DATA'] = pd.to_datetime(df_cotacao_dolar['DATA'], dayfirst=True)
df_cotacao_dolar['Taxa de câmbio - R$ / US$ - comercial - compra - média'] = df_cotacao_dolar['Taxa de câmbio - R$ / US$ - comercial - compra - média'].str.replace(",", ".").astype("float")

# Mesclando os dataframes
df_merge = pd.merge(
    df_preco_petroleo[['DATA', 'Preço - petróleo bruto - Brent (FOB)']],
    df_cotacao_dolar,
    on='DATA',
    how='left'
)

# Criação das abas
abas = st.tabs(["Visão Geral", "Análise do Petróleo", "Análise do Dólar", "Correlação", "Estatísticas Descritivas"])

# Aba 1: Visão Geral
with abas[0]:
    st.subheader('Visualização dos Dados Mesclados')
    st.write("""
    A tabela abaixo apresenta os dados mesclados do preço do petróleo Brent e da cotação do dólar em relação ao real.
    """)
    st.dataframe(df_merge.head())

# Aba 2: Análise do Petróleo
with abas[1]:
    st.subheader('Preço do Petróleo Brent ao Longo do Tempo')
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(df_merge['DATA'], df_merge['Preço - petróleo bruto - Brent (FOB)'], color='blue')
    ax1.set_xlabel('Data')
    ax1.set_ylabel('Preço em USD')
    ax1.set_title('Preço do Petróleo Brent')
    st.pyplot(fig1)

# Aba 3: Análise do Dólar
with abas[2]:
    st.subheader('Cotação do Dólar ao Longo do Tempo')
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.plot(df_merge['DATA'], df_merge['Taxa de câmbio - R$ / US$ - comercial - compra - média'], color='green')
    ax2.set_xlabel('Data')
    ax2.set_ylabel('Cotação em R$')
    ax2.set_title('Cotação do Dólar')
    st.pyplot(fig2)

# Aba 4: Correlação
with abas[3]:
    st.subheader('Análise de Correlação')
    st.write("""
    Nesta seção, analisamos a correlação entre o preço do petróleo Brent e a cotação do dólar.
    """)
    # Calculando a correlação
    df_correlation = df_merge[['Preço - petróleo bruto - Brent (FOB)', 'Taxa de câmbio - R$ / US$ - comercial - compra - média']].dropna()
    correlation = df_correlation.corr()
    st.write('**Matriz de Correlação:**')
    st.dataframe(correlation)

    # Gráfico de dispersão
    fig3, ax3 = plt.subplots(figsize=(8, 6))
    ax3.scatter(df_correlation['Preço - petróleo bruto - Brent (FOB)'], df_correlation['Taxa de câmbio - R$ / US$ - comercial - compra - média'], alpha=0.7)
    ax3.set_xlabel('Preço do Petróleo Brent (USD)')
    ax3.set_ylabel('Cotação do Dólar (R$)')
    ax3.set_title('Correlação entre Petróleo e Dólar')
    st.pyplot(fig3)

# Aba 5: Estatísticas Descritivas
with abas[4]:
    st.subheader('Estatísticas Descritivas')
    st.write("""
    As estatísticas descritivas fornecem um resumo das características dos dados, incluindo medidas de tendência central e dispersão.
    """)
    st.write('**Preço do Petróleo Brent:**')
    st.dataframe(df_merge['Preço - petróleo bruto - Brent (FOB)'].describe())

    st.write('**Cotação do Dólar:**')
    st.dataframe(df_merge['Taxa de câmbio - R$ / US$ - comercial - compra - média'].describe())
