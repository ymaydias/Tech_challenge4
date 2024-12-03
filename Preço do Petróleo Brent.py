import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Análise exploratória: Preço do petróleo bruto Brent.')

st.write("""
O petróleo bruto Brent é um dos principais benchmarks para o preço do petróleo globalmente. Compreender sua evolução ao longo do tempo é crucial para tomadas de decisão.
Aqui, exploraremos os fatores que influenciam o preço do petróleo Brent, examinaremos dados históricos e utilizaremos modelos preditivos para prever tendências futuras, para que assim, importantes insights sejam gerados.
""")

# Leitura dos dados
df_preco_petroleo = pd.read_csv('tabela_dxgvTable.csv', encoding="windows-1252", sep=";")
df_preco_petroleo = df_preco_petroleo.dropna()
df_preco_petroleo['DATA'] = pd.to_datetime(df_preco_petroleo['DATA'], dayfirst=True)
df_preco_petroleo["Preço"] = df_preco_petroleo["Preço - petróleo bruto - Brent (FOB)"].str.replace(",", ".").astype("float")

# Ordenar os dados por data
df_preco_petroleo = df_preco_petroleo.sort_values('DATA').reset_index(drop=True)

# Seção de filtros
st.subheader('Filtro de Data')

# Filtro de intervalo de datas usando um slider
data_minima = df_preco_petroleo['DATA'].min().to_pydatetime()
data_maxima = df_preco_petroleo['DATA'].max().to_pydatetime()

data_inicial, data_final = st.slider(
    'Selecione o intervalo de datas:',
    min_value=data_minima,
    max_value=data_maxima,
    value=(data_minima, data_maxima),
    format="DD/MM/YYYY"
)

# Filtrar os dados com base na data selecionada
df_filtrado = df_preco_petroleo[
    (df_preco_petroleo['DATA'] >= data_inicial) &
    (df_preco_petroleo['DATA'] <= data_final)
].reset_index(drop=True)

# Verificar se o dataframe filtrado não está vazio
if df_filtrado.empty:
    st.warning('Nenhum dado disponível para os filtros selecionados.')
else:
    # Criar o gráfico interativo com Plotly
    fig = px.line(
        df_filtrado,
        x='DATA',
        y='Preço',
        labels={'DATA': 'Data', 'Preço': 'Preço em USD'},
        template='simple_white',
        color_discrete_sequence=['#FF69B4']
    )

    # Ajustar o layout do gráfico
    fig.update_layout(
        title={
            'text': 'Preço do Petróleo Brent',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 24}
        },
        xaxis_title='Data',
        yaxis_title='Preço em USD',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        plot_bgcolor='rgba(0,0,0,0)',
        height=600,
        margin=dict(l=50, r=50, t=100, b=50)
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # Calcular o valor máximo e mínimo no período selecionado
    valor_maximo = df_filtrado['Preço'].max()
    data_valor_maximo = df_filtrado.loc[df_filtrado['Preço'].idxmax(), 'DATA'].strftime('%d/%m/%Y')
    valor_minimo = df_filtrado['Preço'].min()
    data_valor_minimo = df_filtrado.loc[df_filtrado['Preço'].idxmin(), 'DATA'].strftime('%d/%m/%Y')

    # Exibir os valores abaixo do gráfico com estilo personalizado
    st.write("---")
    st.markdown(
        f"""
        <style>
        .card {{
            padding: 1.5em;
            margin: 1em 0;
            border-radius: 10px;
            background-color: #f0f2f6;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        }}
        .card h3 {{
            margin-top: 0;
            color: #333;
        }}
        .max {{
            border-left: 6px solid #FF69B4;
        }}
        .min {{
            border-left: 6px solid #6495ED;
        }}
        .card p {{
            font-size: 1.2em;
            color: #555;
        }}
        </style>
        <div class="card max">
            <h3>📈 Valor Máximo no Período</h3>
            <p><strong>USD {valor_maximo:.2f}</strong> em {data_valor_maximo}</p>
        </div>
        <div class="card min">
            <h3>📉 Valor Mínimo no Período</h3>
            <p><strong>USD {valor_minimo:.2f}</strong> em {data_valor_minimo}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

