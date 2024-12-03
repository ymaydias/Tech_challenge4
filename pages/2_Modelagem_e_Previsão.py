import streamlit as st
import pandas as pd
import numpy as np
from prophet import Prophet
from sklearn.metrics import mean_squared_error, mean_absolute_error
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Modelagem e Previsão", layout="wide")

st.title('📈 Modelagem e Previsão do Preço do Petróleo Brent')

st.write("""

O modelo de previsão desenvolvido com o **Prophet**, conforme abaixo, fornece insights valiosos, embora seja importante considerar que previsões financeiras estão sujeitas a incertezas.


""")

def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    non_zero = y_true != 0
    return np.mean(np.abs((y_true[non_zero] - y_pred[non_zero]) / y_true[non_zero])) * 100

@st.cache_data
def load_petroleo_data(file_path):
    try:
        df = pd.read_csv(file_path, encoding="windows-1252", sep=";")
    except FileNotFoundError:
        st.error(f"O arquivo '{file_path}' não foi encontrado. Por favor, verifique se o arquivo está no diretório correto.")
        st.stop()
    df = df.dropna()
    df['DATA'] = pd.to_datetime(df['DATA'], dayfirst=True)
    df["Preço"] = df["Preço - petróleo bruto - Brent (FOB)"].str.replace(",", ".").astype("float")
    df = df[['DATA', 'Preço']]
    return df

df_preco_petroleo = load_petroleo_data('tabela_dxgvTable.csv')

df_preco_petroleo_renomeado = df_preco_petroleo.rename(columns={'DATA': 'ds', 'Preço': 'y'})

df_preco_petroleo_renomeado = df_preco_petroleo_renomeado[
    (df_preco_petroleo_renomeado['ds'] >= '2019-11-25') &
    (df_preco_petroleo_renomeado['ds'] <= '2024-11-25')
]

split_date = '2023-11-25'
df_train_prophet = df_preco_petroleo_renomeado[df_preco_petroleo_renomeado['ds'] <= split_date].copy()
df_test_prophet = df_preco_petroleo_renomeado[df_preco_petroleo_renomeado['ds'] > split_date].copy()

model = Prophet(daily_seasonality=True)
model.fit(df_train_prophet)

df_test_fcst = model.predict(df_test_prophet)

previsao = df_test_fcst[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

rmse = np.sqrt(mean_squared_error(y_true=df_test_prophet['y'], y_pred=df_test_fcst['yhat']))
mae = mean_absolute_error(y_true=df_test_prophet['y'], y_pred=df_test_fcst['yhat'])
mape = mean_absolute_percentage_error(y_true=df_test_prophet['y'], y_pred=df_test_fcst['yhat'])

df_real = pd.concat([df_train_prophet, df_test_prophet])

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df_real['ds'],
    y=df_real['y'],
    mode='lines',
    name='Valores Reais',
    line=dict(color='#6495ED')
))

fig.add_trace(go.Scatter(
    x=previsao['ds'],
    y=previsao['yhat'],
    mode='lines',
    name='Previsões',
    line=dict(color='#FF69B4')
))

fig.add_trace(go.Scatter(
    x=previsao['ds'],
    y=previsao['yhat_upper'],
    mode='lines',
    name='Intervalo de Confiança Superior',
    line=dict(color='#FF69B4', width=0),
    showlegend=False
))

fig.add_trace(go.Scatter(
    x=previsao['ds'],
    y=previsao['yhat_lower'],
    mode='lines',
    name='Intervalo de Confiança Inferior',
    line=dict(color='#FF69B4', width=0),
    fill='tonexty',
    fillcolor='rgba(255,105,180,0.2)',
    showlegend=False
))

for cp in model.changepoints:
    fig.add_vline(x=cp, line=dict(color='black', dash='dash'), opacity=0.5)

fig.update_layout(
    title={
        'text': '📈 Previsão do Preço do Petróleo Bruto Brent (FOB)',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 24}
    },
    xaxis_title='🗓️ Data',
    yaxis_title='💲 Preço (USD)',
    legend=dict(x=0.01, y=0.99),
    template='plotly_white',
    height=600
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📊 Métricas de Desempenho do Modelo")
st.markdown(f"""
- **Erro Quadrático Médio (RMSE):** {rmse:.2f}
- **Erro Absoluto Médio (MAE):** {mae:.2f}
- **Erro Percentual Absoluto Médio (MAPE):** {mape:.2f}%
""")

st.subheader("📉 Componentes da Série Temporal")

fig_trend = px.line(df_test_fcst, x='ds', y='trend', title='🔄 Trend')
fig_trend.update_layout(
    xaxis_title='🗓️ Data',
    yaxis_title='📈 Trend',
    template='plotly_white',
    height=400
)

fig_weekly = px.line(df_test_fcst, x='ds', y='weekly', title='📅 Sazonalidade Semanal')
fig_weekly.update_layout(
    xaxis_title='🗓️ Data',
    yaxis_title='📆 Weekly',
    template='plotly_white',
    height=400
)

fig_yearly = px.line(df_test_fcst, x='ds', y='yearly', title='🌐 Sazonalidade Anual')
fig_yearly.update_layout(
    xaxis_title='🗓️ Data',
    yaxis_title='📆 Yearly',
    template='plotly_white',
    height=400
)

st.plotly_chart(fig_trend, use_container_width=True)
st.plotly_chart(fig_weekly, use_container_width=True)
st.plotly_chart(fig_yearly, use_container_width=True)


st.markdown(f"""
### 1. 🔍 **Desempenho do Modelo de Previsão**
    
O modelo **Prophet** apresentou as seguintes métricas de desempenho no conjunto de teste:
    
- **Erro Quadrático Médio (RMSE):** {rmse:.2f}
- **Erro Absoluto Médio (MAE):** {mae:.2f}
- **Erro Percentual Absoluto Médio (MAPE):** {mape:.2f}%
    
Estas métricas indicam que o modelo possui uma precisão razoável na previsão dos preços do petróleo Brent. O **RMSE** e o **MAE** fornecem uma medida da magnitude dos erros de previsão, enquanto o **MAPE** oferece uma perspectiva percentual da precisão relativa das previsões.

- O modelo é capaz de capturar a tendência geral dos preços, mas ainda apresenta variações que podem ser atribuídas a fatores não incluídos no modelo.
- O **MAPE** sugere que, em média, as previsões estão a **{mape:.2f}%** do valor real, o que é aceitável para séries temporais financeiras altamente voláteis.
    
""")

st.markdown("""
---
### 2. 🌟 **Identificação de Pontos de Mudança Significativos**
    
O **Prophet** identificou vários pontos de mudança (changepoints) ao longo da série temporal dos preços do petróleo Brent. Estes pontos indicam mudanças significativas na tendência dos preços, que podem estar associadas a eventos específicos no mercado ou na geopolítica.
    
- **Sensibilidade a Eventos:** O modelo é sensível a mudanças abruptas nos preços, capturando rapidamente as novas tendências após eventos disruptivos.
- **Análise de Tendências:** A identificação dos changepoints permite uma análise mais detalhada das causas subjacentes às mudanças nos preços, facilitando a compreensão das dinâmicas do mercado.
    
""")

st.markdown("""
---
### 3. 📉 **Limitações do Modelo de Regressão Linear**
    
Embora o modelo de regressão linear desenvolvido explique aproximadamente **22.33%** da variação na cotação do dólar com base nos preços do petróleo Brent, o coeficiente de determinação (**R²**) relativamente baixo indica que outros fatores econômicos, políticos e sociais também influenciam a taxa de câmbio. Para aprimorar o modelo, é recomendável incorporar variáveis macroeconômicas adicionais, como taxas de juros, inflação e indicadores econômicos globais.
    
- **Fatores Multivariados:** A cotação do dólar é influenciada por múltiplos fatores além dos preços do petróleo.
- **Limitações do Modelo Atual:** O modelo atual possui limitações na captura da complexidade das relações econômicas.
    
""")

st.markdown("""
---
### 4. 💡 **Implicações Estratégicas para Investidores e Policymakers**
    
As previsões fornecidas pelo modelo podem auxiliar investidores e formuladores de políticas na tomada de decisões informadas. Compreender as tendências futuras dos preços do petróleo Brent pode orientar estratégias de investimento e políticas econômicas, permitindo uma melhor gestão de riscos e aproveitamento de oportunidades no mercado energético.
    
- **Planejamento Financeiro:** Investidores podem utilizar as previsões para ajustar suas estratégias de investimento, considerando períodos de alta e baixa nos preços do petróleo.
- **Políticas Econômicas:** Governos e entidades reguladoras podem basear suas políticas energéticas e econômicas nas tendências previstas, visando estabilizar o mercado e mitigar riscos.

""")