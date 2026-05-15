import streamlit as st
import pandas as pd
import os
# Importando suas classes existentes
from modelo.bar.cardPlataformasPublicidades import CardPlataformasPublicidades
from modelo.regressao.regressaoLinear import RegressaoLinear
from modelo.heatmap.correlacaoHeatmap import CorrelacaoHeatmap

# Configuração da página estilo Looqbox
st.set_page_config(page_title="Looqbox Agent Replica", layout="wide")

st.title("🤖 Agente de Dados Looqbox (Replica)")
st.markdown("---")

# Carregamento dos dados (Backend)
@st.cache_data
def carregar_dados():
    caminho = os.path.join("notebooks", "raw", "banco.csv")
    return pd.read_csv(caminho)

base_marketing = carregar_dados()

# Interface de Chat
prompt = st.chat_input("Digite sua dúvida (ex: 'Quero um insight' ou 'Comparativo')")

if prompt:
    st.chat_message("user").write(prompt)
    
    with st.chat_message("assistant"):
        st.write("🔎 Analisando a estrutura dos dados...")
        
        # Lógica de decisão do Agente baseada em suas classes
        if "comparativo" in prompt.lower():
            st.write("Gerando comparativo de plataformas...")
            analise = CardPlataformasPublicidades(base_marketing)
            # Aqui chamamos o método que gera o gráfico na sua classe
            fig = analise.plataformas_publicidades() 
            st.pyplot(fig) # Exibe no 'Canvas' do Streamlit
            
        elif "insight" in prompt.lower() or "prever" in prompt.lower():
            st.write("Calculando modelo preditivo de vendas...")
            regressao = RegressaoLinear(base_marketing)
            y_test, y_pred = regressao.regressao()
            # Integração com sua classe de plotagem preditiva
            st.success("Insight gerado com sucesso!")
            
        elif "correlação" in prompt.lower() or "heatmap" in prompt.lower():
            st.write("Gerando matriz de correlação...")
            heatmap = CorrelacaoHeatmap(base_marketing)
            fig = heatmap.heatmap()
            st.pyplot(fig)
            
        else:
            st.info("Ainda estou aprendendo! Tente perguntar por 'comparativo', 'correlação' ou 'insight'.")