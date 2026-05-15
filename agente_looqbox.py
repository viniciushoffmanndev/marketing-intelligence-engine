import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from openai import OpenAI

# 1. Carregamento de Variáveis de Ambiente e Classes
from modelo.bar.cardPlataformasPublicidades import CardPlataformasPublicidades
from modelo.heatmap.correlacaoHeatmap import CorrelacaoHeatmap
from modelo.regressao.regressaoLinear import RegressaoLinear

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 2. Configuração da Interface (Apenas uma vez!)
st.set_page_config(page_title="Vinicius Pais Agent", layout="wide")

st.title("Agente de Dados Vinicius Pais")
st.markdown("---")

# 3. Sidebar informativa
with st.sidebar:
    st.header("Status do Agente")
    st.success("Conectado à base: banco.csv")
    st.info("Habilidades: Regressão, Heatmaps e Análise de Investimento")

# 4. Backend: Carregamento dos dados
@st.cache_data
def carregar_dados():
    caminho = os.path.join("notebooks", "raw", "banco.csv")
    return pd.read_csv(caminho)

base_marketing = carregar_dados()

# 5. Interface de Chat
prompt = st.chat_input("Como posso ajudar com os dados de marketing hoje?")

if prompt:
    st.chat_message("user").write(prompt)
    
    with st.chat_message("assistant"):
        p_lower = prompt.lower()
        st.write("Analisando a estrutura dos dados...")

        # Lógica Unificada de Decisão
        if "comparativo" in p_lower or "investimento" in p_lower:
            st.write("Analisando investimentos por plataforma...")
            obj = CardPlataformasPublicidades(base_marketing)
            st.pyplot(obj.plataformas_publicidades())
            
        elif "correlação" in p_lower or "heatmap" in p_lower:
            st.write("Gerando matriz de correlação entre variáveis...")
            obj = CorrelacaoHeatmap(base_marketing)
            st.pyplot(obj.heatmap())
            
        elif "insight" in p_lower or "prever" in p_lower or "vendas" in p_lower:
            st.write("Executando modelo de Regressão Linear para previsão de vendas...")
            obj = RegressaoLinear(base_marketing)
            y_test, y_pred = obj.regressao()
            
            st.metric("Acurácia Simbolizada", f"{len(y_pred)} predições geradas")
            st.success("Modelo treinado e executado com sucesso!")
            
        else:
            # Espaço para o fallback da OpenAI que faremos a seguir
            st.warning("Ainda não conheço esse comando específico. Tente pedir um 'comparativo', 'correlação' ou 'previsão'.")