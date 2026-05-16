import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
from openai import OpenAI

# 1. Setup e Conexão
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Intelligence Engine", layout="wide")

st.title("Agente de Dados")
st.markdown("---")

# 2. Carregamento dos dados
@st.cache_data
def carregar_dados():
    # Mantendo seu caminho original
    caminho = os.path.join("notebooks", "raw", "banco.csv")
    return pd.read_csv(caminho)

base_marketing = carregar_dados()

# 3. Sidebar (Agora mostrando as colunas para conferência)
with st.sidebar:
    st.header("Status do Agente")
    st.success("Base: banco.csv")
    st.write("**Colunas disponíveis:**")
    st.code("\n".join(base_marketing.columns.tolist()))

# 4. Interface de Chat
prompt = st.chat_input("Peça uma análise (ex: 'Gráfico de pizza dos gastos' ou 'Relação YouTube vs Vendas')")

if prompt:
    st.chat_message("user").write(prompt)
    
    with st.chat_message("assistant"):
        st.write("Gerando análise dinâmica...")
        
        # O segredo: Passamos os nomes das colunas para a IA saber o que pode plotar
        colunas = base_marketing.columns.tolist()
        
        system_prompt = f"""
        Você é um Engenheiro de Dados sênior. 
        O usuário tem um DataFrame chamado 'base_marketing' com estas colunas: {colunas}.
        
        Sua tarefa:
        1. Escreva o código Python para responder à pergunta.
        2. Se envolver comparação ou tendência, gere um gráfico usando matplotlib ou seaborn.
        3. Para gráficos: use 'fig, ax = plt.subplots()', configure o gráfico e finalize com 'st.pyplot(fig)'.
        4. Para insights em texto: use 'st.write()' ou 'st.info()'.
        5. NÃO use blocos de código (```python). Retorne apenas o código puro.
        6. O DataFrame 'base_marketing' já está carregado, não tente ler o CSV novamente.
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        
        codigo_gerado = response.choices[0].message.content.strip()

        # O Canvas Dinâmico: Aqui o código da IA toma vida
        try:
            # Criamos um container para a análise não ficar solta
            with st.container(border=True):
                exec(codigo_gerado)
        except Exception as e:
            st.error(f"Erro ao processar os dados: {e}")
            # Em caso de erro, mostramos o código para você debugar
            with st.expander("Ver código gerado"):
                st.code(codigo_gerado)