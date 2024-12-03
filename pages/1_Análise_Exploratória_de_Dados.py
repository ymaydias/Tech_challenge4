import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import pearsonr, spearmanr
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

st.title('📊 Análise Exploratória de Dados')

st.markdown("""
    Bem-vindo à **Análise Exploratória de Dados**! Esta aplicação examina os dados históricos do **Preço do Petróleo Brent** e da **Cotação do Dólar**, identificando outliers e explorando os principais eventos que influenciaram essas variações ao longo das últimas quatro décadas.
""")

@st.cache_data
def load_petroleo_data(file_path):
    try:
        df = pd.read_csv(file_path, encoding="windows-1252", sep=";")
    except FileNotFoundError:
        st.error(f"O arquivo '{file_path}' não foi encontrado. Por favor, verifique se o arquivo está no diretório correto.")
        st.stop()
    df = df.dropna()
    df['DATA'] = pd.to_datetime(df['DATA'], dayfirst=True)
    df["Preço_Petróleo"] = df["Preço - petróleo bruto - Brent (FOB)"].str.replace(",", ".").astype("float")
    df = df[['DATA', 'Preço_Petróleo']]
    return df

@st.cache_data
def load_dolar_data(file_path, coluna_cotacao):
    try:
        df = pd.read_csv(file_path, encoding="windows-1252", sep=";")
    except FileNotFoundError:
        st.error(f"O arquivo '{file_path}' não foi encontrado. Por favor, verifique se o arquivo está no diretório correto.")
        st.stop()
    df = df.dropna()
    df['DATA'] = pd.to_datetime(df['DATA'], dayfirst=True)
    if coluna_cotacao not in df.columns:
        st.error(f"A coluna '{coluna_cotacao}' não foi encontrada no arquivo '{file_path}'. As colunas disponíveis são: {df.columns.tolist()}")
        st.stop()
    df.rename(columns={coluna_cotacao: 'Cotacao_Dolar'}, inplace=True)
    df['Cotacao_Dolar'] = df['Cotacao_Dolar'].str.replace(",", ".").astype("float")
    df = df[['DATA', 'Cotacao_Dolar']]
    return df

df_petroleo = load_petroleo_data('tabela_dxgvTable.csv')
df_dolar = load_dolar_data('tabela_dxgvTable_dolar.csv', 'Taxa de câmbio - R$ / US$ - comercial - compra - média')

aba1, aba2 = st.tabs(["💱 Dólar vs Petróleo", "📈 Dados Históricos"])

with aba1:
    st.header("💱 Análise de Dólar vs Petróleo")
    st.markdown("---")
    
    df_combinado = pd.merge(df_petroleo, df_dolar, on='DATA', how='inner')
    df_combinado = df_combinado.sort_values('DATA').reset_index(drop=True)
    
    if df_combinado.empty:
        st.warning('Nenhum dado disponível após combinar os dados de petróleo e dólar. Verifique se as datas nos dois arquivos coincidem.')
    else:
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df_combinado['DATA'],
            y=df_combinado['Preço_Petróleo'],
            mode='lines',
            name='Preço do Petróleo Brent (USD)',
            line=dict(color='#FF69B4')
        ))

        fig.add_trace(go.Scatter(
            x=df_combinado['DATA'],
            y=df_combinado['Cotacao_Dolar'],
            mode='lines',
            name='Cotação do Dólar (BRL)',
            line=dict(color='#6495ED'),
            yaxis='y2'
        ))

        fig.update_layout(
            title={
                'text': '📈 Preço do Petróleo Brent vs. Cotação do Dólar',
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title='🗓️ Data',
            yaxis_title='💲 Preço do Petróleo Brent (USD)',
            yaxis=dict(title='💲 Preço do Petróleo Brent (USD)', showgrid=False),
            yaxis2=dict(
                title='💱 Cotação do Dólar (BRL)',
                overlaying='y',
                side='right',
                showgrid=False
            ),
            legend=dict(x=0.01, y=0.99),
            height=600,
            margin=dict(l=50, r=50, t=100, b=50),
            plot_bgcolor='rgba(0,0,0,0)'
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("🔍 Análise de Correlação")
        st.markdown("")

        pearson_corr, pearson_p = pearsonr(df_combinado['Preço_Petróleo'], df_combinado['Cotacao_Dolar'])
        st.write(f"**📏 Coeficiente de Correlação de Pearson:** {pearson_corr:.4f} (p-valor: {pearson_p:.4e})")

        spearman_corr, spearman_p = spearmanr(df_combinado['Preço_Petróleo'], df_combinado['Cotacao_Dolar'])
        st.write(f"**📊 Coeficiente de Correlação de Spearman:** {spearman_corr:.4f} (p-valor: {spearman_p:.4e})")

        st.markdown("""
        📈 **Coeficiente de Pearson**: Indica uma correlação positiva moderada entre o preço do petróleo Brent e a cotação do dólar. Isso sugere que, em geral, quando o preço do petróleo aumenta, a cotação do dólar também tende a subir.

        📉 **Coeficiente de Spearman**: Revela uma correlação positiva moderada a forte, indicando uma relação monotônica entre as duas variáveis. Ambos os coeficientes possuem p-valores próximos de zero, demonstrando que as correlações são estatisticamente significativas.
        """)

        st.subheader("📉 Análise de Regressão Linear")
        st.markdown("")

        fig_scatter = px.scatter(
            df_combinado,
            x='Preço_Petróleo',
            y='Cotacao_Dolar',
            trendline='ols',
            labels={
                'Preço_Petróleo': '💲 Preço do Petróleo Brent (USD)',
                'Cotacao_Dolar': '💱 Cotação do Dólar (BRL)'
            },
            title='📈 Relação entre o Preço do Petróleo Brent e a Cotação do Dólar'
        )

        st.plotly_chart(fig_scatter, use_container_width=True)

        results = px.get_trendline_results(fig_scatter)
        modelo_ols = results.px_fit_results.iloc[0].summary()
        st.text(modelo_ols)

        st.markdown("""
        📐 **Coeficiente Angular (Slope)**: Indica a variação esperada na cotação do dólar para cada unidade de aumento no preço do petróleo. 

        📏 **Intercepto**: Representa o valor esperado da cotação do dólar quando o preço do petróleo é zero.

        📈 **R² (Coeficiente de Determinação)**: Aproximadamente **22.33%** da variação na cotação do dólar pode ser explicada pelo modelo linear com o preço do petróleo. Embora não seja alto, indica que o modelo capta uma parte significativa da relação entre as variáveis.

        **Nota:** O preço do petróleo é apenas um dos diversos fatores que influenciam a cotação do dólar. Outros elementos econômicos, políticos e sociais também desempenham papéis importantes.
        """)

with aba2:
    st.header("📈 Análise de Dados Históricos do Preço do Petróleo Brent")
    st.markdown("---")
    
    st.subheader("🔍 Detecção de Outliers no Preço do Petróleo Brent")
    st.markdown("")

    window_size = 12

    df_petroleo['Rolling_Mean'] = df_petroleo['Preço_Petróleo'].rolling(window=window_size, center=True).mean()
    df_petroleo['Rolling_STD'] = df_petroleo['Preço_Petróleo'].rolling(window=window_size, center=True).std()
    df_petroleo['Z_Score'] = (df_petroleo['Preço_Petróleo'] - df_petroleo['Rolling_Mean']) / df_petroleo['Rolling_STD']
    df_petroleo['Outlier'] = df_petroleo['Z_Score'].abs() > 2
    df_petroleo_outliers = df_petroleo.dropna(subset=['Z_Score'])
    normais_petroleo = df_petroleo_outliers[df_petroleo_outliers['Outlier'] == False]
    outliers_petroleo = df_petroleo_outliers[df_petroleo_outliers['Outlier'] == True]

    eventos_petroleo_df = pd.DataFrame({
        'DATA': [
            '1979-12-01',
            '1986-06-01',
            '1990-10-01',
            '1998-02-01',
            '2008-07-01',
            '2011-05-01',
            '2014-06-01',
            '2020-04-01'
        ],
        'Evento_Descricao': [
            '📌 **Revolução Iraniana**: Redução drástica na produção de petróleo do Irã, causando escassez no mercado global e elevando os preços do petróleo Brent.',
            '📌 **Acordo Plaza**: Coordenação das nações desenvolvidas e da OPEP para depreciar o dólar americano, resultando em queda significativa nos preços do petróleo.',
            '📌 **Guerra do Golfo**: Instabilidade na região do Golfo Pérsico provocou preocupações sobre interrupções no fornecimento, elevando os preços do petróleo Brent.',
            '📌 **Crise Asiática**: Desaceleração econômica global reduziu a demanda por petróleo, contribuindo para a queda nos preços do petróleo Brent.',
            '📌 **Pico dos Preços em 2008**: Combinação de alta demanda global, instabilidades geopolíticas e especulação levou os preços do petróleo Brent a níveis recordes antes da crise financeira.',
            '📌 **Primavera Árabe**: Instabilidade política em países produtores de petróleo no Oriente Médio e Norte da África levou a flutuações nos preços devido a temores de interrupções no fornecimento.',
            '📌 **Queda de 2014-2016**: Aumento da produção de petróleo de xisto nos EUA e decisão da OPEP de manter altos níveis de produção resultaram em excesso de oferta e queda nos preços do petróleo Brent.',
            '📌 **Pandemia de COVID-19**: Restrições de mobilidade e redução da atividade econômica global levaram a uma queda histórica nos preços do petróleo Brent, atingindo níveis próximos de US$ 20 por barril.'
        ]
    })

    eventos_petroleo_df['DATA'] = pd.to_datetime(eventos_petroleo_df['DATA'])
    outliers_petroleo = pd.merge(outliers_petroleo, eventos_petroleo_df, on='DATA', how='left')
    outliers_petroleo['Evento_Descricao'].fillna("🔍 Sem Evento Identificado", inplace=True)

    st.markdown("")

    fig_petroleo = go.Figure()

    fig_petroleo.add_trace(go.Scatter(
        x=normais_petroleo['DATA'],
        y=normais_petroleo['Preço_Petróleo'],
        mode='lines',
        name='Normal',
        line=dict(color='lightgray'),
        showlegend=False
    ))

    fig_petroleo.add_trace(go.Scatter(
        x=outliers_petroleo['DATA'],
        y=outliers_petroleo['Preço_Petróleo'],
        mode='markers',
        name='Outlier',
        marker=dict(color='red', size=10, symbol='circle'),
        text=outliers_petroleo['Evento_Descricao'],
        hoverinfo='text',
        showlegend=True
    ))

    fig_petroleo.update_layout(
        xaxis_title='🗓️ Data',
        yaxis_title='💲 Preço do Petróleo Brent (USD)',
        hovermode='closest',
        height=600,
        margin=dict(l=50, r=50, t=80, b=50),
        plot_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig_petroleo, use_container_width=True)

    st.subheader("📋 Tabela de Outliers no Preço do Petróleo Brent")
    st.markdown("")

    outliers_petroleo['DATA'] = outliers_petroleo['DATA'].dt.strftime('%Y-%m-%d')

    st.markdown("""
    <div style="height: 300px; overflow: auto;">
        {table}
    </div>
    """.format(table=outliers_petroleo[['DATA', 'Preço_Petróleo']].to_html(index=False, classes='dataframe')),
                unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📝 Análise dos Principais Eventos que Influenciaram os Outliers no Preço do Petróleo Brent")
    st.markdown("")

    st.markdown("""
    Os outliers identificados no preço do petróleo Brent refletem momentos de extrema volatilidade e são frequentemente associados a eventos significativos que afetam a oferta e a demanda global de petróleo. A seguir, destacamos os principais acontecimentos e tendências que contribuíram para esses desvios ao longo das últimas quatro décadas.
    """)

    analise_texto = """
    ### **1. Crise do Petróleo de 1973 e 1979**
    
    - **1973:** A crise do petróleo de 1973 foi desencadeada pelo embargo da OPEP aos países que apoiaram Israel durante a Guerra do Yom Kippur. Isso resultou em um aumento drástico nos preços do petróleo, impactando severamente as economias ocidentais.
    
    - **1979:** A Revolução Iraniana levou à redução significativa na produção de petróleo do Irã, causando escassez no mercado global. Os preços do petróleo Brent dispararam, refletindo a instabilidade geopolítica na região.
    
    ### **2. Guerra do Golfo de 1990-1991**
    
    A invasão do Kuwait pelo Iraque em agosto de 1990 resultou na Guerra do Golfo em 1991. A instabilidade no Golfo Pérsico, uma das principais regiões produtoras de petróleo, gerou preocupações sobre interrupções no fornecimento global, elevando os preços do petróleo Brent.
    
    ### **3. Crise Financeira Asiática de 1997-1998**
    
    A crise financeira que atingiu vários países asiáticos levou a uma desaceleração econômica global, reduzindo a demanda por petróleo. Esse excesso de oferta combinado com a queda da demanda resultou em uma queda significativa nos preços do petróleo Brent.
    
    ### **4. Guerra do Iraque de 2003**
    
    A invasão do Iraque pelos Estados Unidos e aliados em 2003 causou instabilidade contínua na região do Golfo Pérsico. A incerteza sobre a produção e a distribuição de petróleo contribuiu para flutuações nos preços do petróleo Brent.
    
    ### **5. Crise Financeira Global de 2008**
    
    A crise financeira de 2008 levou a uma forte recessão econômica global. A redução da atividade econômica diminuiu a demanda por petróleo, resultando em uma queda abrupta nos preços do petróleo Brent após um período de alta.
    
    ### **6. Queda dos Preços do Petróleo de 2014-2016**
    
    A partir de 2014, houve um aumento na produção de petróleo de xisto nos Estados Unidos, aliado à decisão da OPEP de manter altos níveis de produção para preservar sua participação no mercado. Esse excesso de oferta global fez com que os preços do petróleo Brent caíssem drasticamente.
    
    ### **7. Pandemia de COVID-19 de 2020**
    
    A pandemia de COVID-19 levou a restrições de mobilidade e uma redução sem precedentes na atividade econômica global. A queda na demanda por petróleo resultou em uma queda histórica nos preços do petróleo Brent, atingindo níveis próximos de US$ 20 por barril.
    
    ### **8. Transição Energética e Investimentos em Energias Renováveis**
    
    Nos últimos anos, a crescente conscientização sobre as mudanças climáticas e os investimentos em energias renováveis têm influenciado a demanda por petróleo. A transição energética está começando a impactar os preços e a dinâmica do mercado do petróleo Brent.
    
    ### **9. Decisões da OPEP e Aliados (OPEMIA)**
    
    As decisões estratégicas da OPEP e seus aliados, conhecidos como OPEMIA, sobre os níveis de produção têm um papel crucial na determinação dos preços do petróleo Brent. Reduções ou aumentos na produção podem levar a flutuações significativas nos preços.
    
    ### **10. Instabilidades Geopolíticas Contínuas**
    
    Conflitos regionais, sanções econômicas e instabilidades políticas em países produtores de petróleo continuam a influenciar os preços do petróleo Brent, adicionando um elemento de volatilidade ao mercado.
    """

    st.markdown(analise_texto)

 