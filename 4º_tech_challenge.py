# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

#http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view

df_preco_petroleo = pd.read_csv('tabela_dxgvTable.csv', encoding = "windows-1252", sep=";")

df_preco_petroleo = df_preco_petroleo.dropna()

df_preco_petroleo.info()

df_preco_petroleo['DATA'] = pd.to_datetime(df_preco_petroleo['DATA'], dayfirst=True)

df_preco_petroleo["Preço - petróleo bruto - Brent (FOB)"] = df_preco_petroleo["Preço - petróleo bruto - Brent (FOB)"].str.replace(",", ".").astype("float")

df_preco_petroleo.isnull().sum()

df_preco_petroleo.duplicated().sum()

df_preco_petroleo.describe()

#http://www.ipeadata.gov.br/ExibeSerie.aspx?serid=38590&module=M

df_cotacao_dolar = pd.read_csv('tabela_dxgvTable_dolar.csv', encoding = "windows-1252", sep=";")

df_cotacao_dolar.info()

df_cotacao_dolar['DATA'] = pd.to_datetime(df_cotacao_dolar['DATA'], dayfirst=True)

df_cotacao_dolar['Taxa de câmbio - R$ / US$ - comercial - compra - média'] = df_cotacao_dolar['Taxa de câmbio - R$ / US$ - comercial - compra - média'].str.replace(",", ".").astype("float")

df_cotacao_dolar.isnull().sum()

df_cotacao_dolar.duplicated().sum()

df_cotacao_dolar.describe()

df_merge = pd.merge(df_preco_petroleo[['DATA','Preço - petróleo bruto - Brent (FOB)']], df_cotacao_dolar, on = ['DATA'], how = 'left')

df_merge.info()

df_merge

from prophet import Prophet

from sklearn.metrics import mean_squared_error, mean_absolute_error

def mean_absolute_percentage_error(y_true, y_pred):
  y_true, y_pred = np.array(y_true), np.array(y_pred)
  return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

df_preco_petroleo_renomeado = df_preco_petroleo.rename(columns={'DATA': 'ds', 'Preço - petróleo bruto - Brent (FOB)': 'y'})

df_preco_petroleo_renomeado = df_preco_petroleo_renomeado[(df_preco_petroleo_renomeado['ds'] >= '2019-11-25') & (df_preco_petroleo_renomeado['ds'] <= '2024-11-25')]

df_preco_petroleo_renomeado =  df_preco_petroleo_renomeado.set_index('ds')

split_date = '2023-11-25'
df_preco_petroleo_renomeado_train = df_preco_petroleo_renomeado.loc[df_preco_petroleo_renomeado.index <= split_date].copy()
df_preco_petroleo_renomeado_test = df_preco_petroleo_renomeado.loc[df_preco_petroleo_renomeado.index > split_date].copy()

df_train_prophet = df_preco_petroleo_renomeado_train.reset_index()

model = Prophet(daily_seasonality=True)
model.fit(df_train_prophet)

df_test_prophet = df_preco_petroleo_renomeado_test.reset_index()

df_test_fcst = model.predict(df_test_prophet)

df_test_fcst.head()

previsao = df_test_fcst[['ds', 'yhat']]

previsao

np.sqrt(mean_squared_error(y_true= df_test_prophet['y'], y_pred= df_test_fcst['yhat']))

mean_absolute_error(y_true= df_test_prophet['y'], y_pred= df_test_fcst['yhat'])

mean_absolute_percentage_error(y_true= df_test_prophet['y'], y_pred= df_test_fcst['yhat'])

import matplotlib.pyplot as plt
from prophet.plot import add_changepoints_to_plot
fig = model.plot(df_test_fcst)
mudancas = add_changepoints_to_plot(fig.gca(), model, df_test_fcst)
ax = fig.gca()
for line in ax.get_lines()[2:]:
    line.set_color('black')
ax.set_title('Previsão - Preço - petróleo bruto - Brent (FOB)')
ax.set_xlabel('Data')
ax.set_ylabel('Preço - petróleo bruto - Brent (FOB)')
plt.show()

model.changepoints
