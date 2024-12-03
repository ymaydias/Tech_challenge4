# pages/3_Modelagem_e_Previsão.py

import streamlit as st
import pandas as pd
import numpy as np
from prophet import Prophet
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt
from prophet.plot import add_changepoints_to_plot
import joblib

st.title('Modelagem e Previsão')

st.write("""
Utilizamos o modelo Prophet para prever o preço futuro do petróleo Brent. Nesta seção, apresentamos o processo de modelagem, as previsões geradas e as métricas de avaliação do modelo.
""")

# Função para calcular o MAPE
def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

# Leitura e preparação dos dados (mesmos passos anteriores)
df_preco_petroleo = pd.read_csv('tabela_dxgvTable.csv', encoding="windows-1252", sep=";")
df_preco_petroleo = df_preco_petroleo.dropna()
df_preco_petroleo['DATA'] = pd.to_datetime(df_preco_petroleo['DATA'], dayfirst=True)
df_preco_petroleo["Preço - petróleo bruto - Brent (FOB)"] = df_preco_petroleo["Preço - petróleo bruto - Brent (FOB)"].str.replace(",", ".").astype("float")

# Preparando os dados para o Prophet
df_prophet = df_preco_petroleo.rename(columns={'DATA': 'ds', 'Preço - petróleo bruto - Brent (FOB)': 'y'})
df_prophet = df_prophet[(df_prophet['ds'] >= '2019-11-25') & (df_prophet['ds'] <= '2024-11-25')]
df_prophet = df_prophet.set_index('ds')

# Dividindo os dados em treino e teste
split_date = '2023-11-25'
df_train = df_prophet.loc[df_prophet.index <= split_date].copy()
df_test = df_prophet.loc[df_prophet.index > split_date].copy()

# Treinando o modelo Prophet
df_train_prophet = df_train.reset_index()
model = Prophet(daily_seasonality=True)
model.fit(df_train_prophet)

# Fazendo previsões
df_test_prophet = df_test.reset_index()
forecast = model.predict(df_test_prophet)
previsao = forecast[['ds', 'yhat']]

st.subheader('Previsão do Modelo')
st.dataframe(previsao)

# Calculando métricas de erro
rmse = np.sqrt(mean_squared_error(y_true=df_test_prophet['y'], y_pred=forecast['yhat']))
mae = mean_absolute_error(y_true=df_test_prophet['y'], y_pred=forecast['yhat'])
mape = mean_absolute_percentage_error(y_true=df_test_prophet['y'], y_pred=forecast['yhat'])

st.subheader('Métricas de Avaliação do Modelo')
st.write(f'**RMSE:** {rmse:.2f}')
st.write(f'**MAE:** {mae:.2f}')
st.write(f'**MAPE:** {mape:.2f}%')

# Plotando a previsão
st.subheader('Gráfico da Previsão')
fig1 = model.plot(forecast)
add_changepoints_to_plot(fig1.gca(), model, forecast)
st.pyplot(fig1)

# Salvando o modelo
joblib.dump(model, 'Prophet.joblib')
st.success('Modelo salvo como Prophet.joblib')
