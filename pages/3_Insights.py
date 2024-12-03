import streamlit as st

st.subheader("📊 Insights da Análise")

st.markdown("""
### 1. 🔗 **Correlação Positiva Moderada entre Preço do Petróleo e Cotação do Dólar**

A análise de correlação revelou uma relação positiva moderada entre o preço do petróleo Brent e a cotação do dólar americano, com coeficientes de Pearson (0.4725) e Spearman (0.5547). Essa correlação sugere que, em geral, aumentos nos preços do petróleo estão associados a uma valorização do dólar. Essa interdependência pode ser atribuída à demanda por dólares para transações em petróleo, influenciando a taxa de câmbio.

**Conclusões:**
- **Influência Mútua:** Flutuações no preço do petróleo podem afetar diretamente a força do dólar, e vice-versa.
- **Indicador Econômico:** O preço do petróleo pode servir como um indicador para movimentos futuros na taxa de câmbio do dólar.

**Ações Recomendadas:**
- **Monitoramento Contínuo:** Manter um acompanhamento constante das tendências de preços do petróleo e da cotação do dólar para antecipar movimentos de mercado.
- **Diversificação de Portfólio:** Investidores podem considerar diversificar seus portfólios para mitigar riscos associados a essa correlação.
- **Análise Integrada:** Incorporar a análise da cotação do dólar nas estratégias de investimento relacionadas ao petróleo.

---

### 2. 🌍 **Impacto Significativo de Eventos Geopolíticos nos Preços do Petróleo**

A detecção de outliers no histórico de preços do petróleo Brent está fortemente ligada a eventos geopolíticos como guerras, revoluções e crises econômicas. Por exemplo, a Revolução Iraniana e a Guerra do Golfo resultaram em aumentos abruptos nos preços devido à interrupção na produção e fornecimento de petróleo. Esses eventos destacam a sensibilidade do mercado petrolífero a instabilidades políticas, ressaltando a importância de monitorar tais acontecimentos para prever flutuações de preços.

**Conclusões:**
- **Volatilidade Externa:** Eventos geopolíticos têm um impacto direto e imediato na volatilidade dos preços do petróleo.
- **Risco de Fornecimento:** Instabilidades em regiões produtoras podem comprometer o fornecimento global, elevando os preços.

**Ações Recomendadas:**
- **Análise de Cenários:** Desenvolver modelos de previsão que considerem diferentes cenários geopolíticos para antecipar possíveis impactos nos preços do petróleo.
- **Estratégias de Mitigação:** Empresas e investidores devem adotar estratégias de mitigação de riscos para proteger-se contra volatilidades causadas por eventos geopolíticos.
- **Engajamento Político:** Policymakers devem buscar estabilizar regiões estratégicas para garantir um fornecimento contínuo e reduzir incertezas no mercado.

---

### 3. 📉 **Poder Preditivo Limitado do Modelo de Regressão Linear**

O modelo de regressão linear desenvolvido explica aproximadamente 22.33% da variação na cotação do dólar com base nos preços do petróleo Brent. Embora a relação seja estatisticamente significativa, o coeficiente de determinação (R²) relativamente baixo indica que outros fatores econômicos, políticos e sociais também influenciam a taxa de câmbio. Para aprimorar o modelo, é recomendável incorporar variáveis macroeconômicas adicionais, como taxas de juros, inflação e indicadores econômicos globais.

**Conclusões:**
- **Fatores Multivariados:** A cotação do dólar é influenciada por múltiplos fatores além dos preços do petróleo.
- **Limitações do Modelo Atual:** O modelo atual possui limitações na captura da complexidade das relações econômicas.

**Ações Recomendadas:**
- **Incorporação de Variáveis:** Integrar variáveis macroeconômicas e indicadores financeiros no modelo para aumentar sua precisão.
- **Modelos Avançados:** Explorar técnicas de modelagem mais sofisticadas, como redes neurais ou modelos ARIMA, para capturar melhor as dinâmicas temporais.
- **Validação e Atualização:** Realizar validações contínuas do modelo com novos dados e ajustar os parâmetros conforme necessário para manter a relevância e a precisão.

---

### 4. 💡 **Implicações Estratégicas para Investidores e Policymakers**

Compreender a correlação e a dinâmica entre os preços do petróleo e a cotação do dólar é essencial para investidores e formuladores de políticas. Para investidores, isso pode orientar estratégias de diversificação e hedge para mitigar riscos associados à volatilidade dos preços do petróleo. Para policymakers, insights sobre essa relação podem informar decisões econômicas, como ajustes na política monetária e medidas para estabilizar a economia diante de flutuações nos preços do petróleo.

**Conclusões:**
- **Tomada de Decisão Informada:** A análise fornece uma base sólida para decisões estratégicas no âmbito financeiro e político.
- **Gestão de Riscos:** Estratégias adequadas podem reduzir a exposição a riscos decorrentes da volatilidade dos preços do petróleo e das flutuações cambiais.

**Ações Recomendadas:**
- **Estratégias de Hedge:** Investidores devem considerar instrumentos financeiros como futuros e opções para proteger-se contra movimentos adversos nos preços do petróleo e na cotação do dólar.
- **Políticas Econômicas Adaptativas:** Policymakers devem desenvolver políticas flexíveis que possam responder rapidamente a mudanças nos mercados de petróleo e câmbio.
- **Educação e Treinamento:** Promover a educação financeira para investidores e a capacitação de policymakers para interpretar e utilizar os insights da análise de forma eficaz.

""")