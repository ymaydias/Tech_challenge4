import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.markdown("""
    <style>
    .css-1aumxhk {
        padding-top: 2rem;
    }
    table.dataframe {
        width: 100%;
        border-collapse: collapse;
    }
    table.dataframe th, table.dataframe td {
        border: 1px solid #ddd;
        padding: 8px;
    }
    table.dataframe tr:nth-child(even){background-color: #f2f2f2;}
    table.dataframe tr:hover {background-color: #ddd;}
    table.dataframe th {
        padding-top: 12px;
        padding-bottom: 12px;
        text-align: left;
        background-color: #4CAF50;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title('📈 Preço do Petróleo Bruto Brent')

st.markdown("""
    O petróleo bruto Brent é um dos principais benchmarks para o preço do petróleo globalmente. Compreender sua evolução ao longo do tempo é crucial para tomadas de decisão.
    Aqui, exploraremos os fatores que influenciam o preço do petróleo Brent, examinaremos dados históricos e utilizaremos modelos preditivos para prever tendências futuras, para que assim, importantes insights sejam gerados.
""")

df_preco_petroleo = pd.read_csv('tabela_dxgvTable.csv', encoding="windows-1252", sep=";")
df_preco_petroleo = df_preco_petroleo.dropna()
df_preco_petroleo['DATA'] = pd.to_datetime(df_preco_petroleo['DATA'], dayfirst=True)
df_preco_petroleo["Preço"] = df_preco_petroleo["Preço - petróleo bruto - Brent (FOB)"].str.replace(",", ".").astype("float")
df_preco_petroleo = df_preco_petroleo.sort_values('DATA').reset_index(drop=True)

st.subheader('🔍 Filtro de Data')

data_minima = df_preco_petroleo['DATA'].min().to_pydatetime()
data_maxima = df_preco_petroleo['DATA'].max().to_pydatetime()

data_inicial, data_final = st.slider(
    'Selecione o intervalo de datas:',
    min_value=data_minima,
    max_value=data_maxima,
    value=(data_minima, data_maxima),
    format="DD/MM/YYYY"
)

df_filtrado = df_preco_petroleo[
    (df_preco_petroleo['DATA'] >= data_inicial) &
    (df_preco_petroleo['DATA'] <= data_final)
].reset_index(drop=True)

if df_filtrado.empty:
    st.warning('Nenhum dado disponível para os filtros selecionados.')
else:
    fig = px.line(
        df_filtrado,
        x='DATA',
        y='Preço',
        labels={'DATA': '🗓️ Data', 'Preço': '💲 Preço em USD'},
        template='simple_white',
        color_discrete_sequence=['#FF69B4']
    )

    fig.update_layout(
        title={
            'text': '📈 Preço do Petróleo Brent',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 24}
        },
        xaxis_title='🗓️ Data',
        yaxis_title='💲 Preço em USD',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        plot_bgcolor='rgba(0,0,0,0)',
        height=600,
        margin=dict(l=50, r=50, t=100, b=50)
    )

    st.plotly_chart(fig, use_container_width=True)

    valor_maximo = df_filtrado['Preço'].max()
    data_valor_maximo = df_filtrado.loc[df_filtrado['Preço'].idxmax(), 'DATA'].strftime('%d/%m/%Y')
    valor_minimo = df_filtrado['Preço'].min()
    data_valor_minimo = df_filtrado.loc[df_filtrado['Preço'].idxmin(), 'DATA'].strftime('%d/%m/%Y')

    st.markdown("""
    <div style="display: flex; gap: 2rem; margin-top: 2rem;">
        <div style="flex: 1; padding: 1.5em; border-radius: 10px; background-color: #e0f7fa; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
            <h3>📈 Valor Máximo no Período</h3>
            <p><strong>USD {valor_maximo:.2f}</strong> em {data_valor_maximo}</p>
        </div>
        <div style="flex: 1; padding: 1.5em; border-radius: 10px; background-color: #ffe0b2; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
            <h3>📉 Valor Mínimo no Período</h3>
            <p><strong>USD {valor_minimo:.2f}</strong> em {data_valor_minimo}</p>
        </div>
    </div>
    """.format(valor_maximo=valor_maximo, data_valor_maximo=data_valor_maximo, valor_minimo=valor_minimo, data_valor_minimo=data_valor_minimo),
    unsafe_allow_html=True)
