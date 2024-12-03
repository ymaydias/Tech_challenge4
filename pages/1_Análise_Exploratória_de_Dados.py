import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title('Análise Exploratória de Dados')

st.write("""
Nesta seção, examinamos os dados históricos do preço do petróleo Brent e da cotação do dólar. A análise exploratória nos ajuda a entender padrões, tendências e possíveis outliers nos dados.
""")

# Leitura dos dados do petróleo
df_petroleo = pd.read_csv('tabela_dxgvTable.csv', encoding="windows-1252", sep=";")
df_petroleo = df_petroleo.dropna()
df_petroleo['DATA'] = pd.to_datetime(df_petroleo['DATA'], dayfirst=True)
df_petroleo["Preço_Petróleo"] = df_petroleo["Preço - petróleo bruto - Brent (FOB)"].str.replace(",", ".").astype("float")
df_petroleo = df_petroleo[['DATA', 'Preço_Petróleo']]

# Leitura dos dados do dólar
try:
    df_dolar = pd.read_csv('tabela_dxgvTable_dolar.csv', encoding="windows-1252", sep=";")
except FileNotFoundError:
    st.error("O arquivo 'tabela_dxgvTable_dolar.csv' não foi encontrado. Por favor, verifique se o arquivo está no diretório correto.")
    st.stop()

df_dolar = df_dolar.dropna()
df_dolar['DATA'] = pd.to_datetime(df_dolar['DATA'], dayfirst=True)

# Atualizar o nome da coluna de cotação do dólar
coluna_cotacao_dolar = 'Taxa de câmbio - R$ / US$ - comercial - compra - média'

# Verificar se a coluna existe no DataFrame
if coluna_cotacao_dolar not in df_dolar.columns:
    st.error(f"A coluna '{coluna_cotacao_dolar}' não foi encontrada no arquivo 'tabela_dxgvTable_dolar.csv'. As colunas disponíveis são: {df_dolar.columns.tolist()}")
    st.stop()

# Renomear a coluna para 'Cotacao_Dolar'
df_dolar.rename(columns={coluna_cotacao_dolar: 'Cotacao_Dolar'}, inplace=True)

# Converter a cotação do dólar para float
df_dolar['Cotacao_Dolar'] = df_dolar['Cotacao_Dolar'].str.replace(",", ".").astype("float")

# Selecionar as colunas necessárias
df_dolar = df_dolar[['DATA', 'Cotacao_Dolar']]

# Combinar os dados com base na data
df_combinado = pd.merge(df_petroleo, df_dolar, on='DATA', how='inner')

# Ordenar por data
df_combinado = df_combinado.sort_values('DATA').reset_index(drop=True)

# Verificar se o DataFrame combinado não está vazio
if df_combinado.empty:
    st.warning('Nenhum dado disponível após combinar os dados de petróleo e dólar. Verifique se as datas nos dois arquivos coincidem.')
else:
    # Criar o gráfico comparativo
    fig = go.Figure()

    # Adicionar a linha do preço do petróleo
    fig.add_trace(go.Scatter(
        x=df_combinado['DATA'],
        y=df_combinado['Preço_Petróleo'],
        mode='lines',
        name='Preço do Petróleo Brent (USD)',
        line=dict(color='#FF69B4')
    ))

    # Adicionar a linha da cotação do dólar
    fig.add_trace(go.Scatter(
        x=df_combinado['DATA'],
        y=df_combinado['Cotacao_Dolar'],
        mode='lines',
        name='Cotação do Dólar (BRL)',
        line=dict(color='#6495ED'),
        yaxis='y2'
    ))

    # Configurar o layout com dois eixos y
    fig.update_layout(
        title={
            'text': 'Preço do Petróleo Brent vs. Cotação do Dólar',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title='Data',
        yaxis_title='Preço do Petróleo Brent (USD)',
        yaxis=dict(title='Preço do Petróleo Brent (USD)', showgrid=False),
        yaxis2=dict(
            title='Cotação do Dólar (BRL)',
            overlaying='y',
            side='right',
            showgrid=False
        ),
        legend=dict(x=0.01, y=0.99),
        height=600,
        margin=dict(l=50, r=50, t=100, b=50),
        plot_bgcolor='rgba(0,0,0,0)'
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)
