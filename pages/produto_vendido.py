import streamlit as st
from utils.database import get_all_produtos
import os

# --- Funções Auxiliares ---

def load_css(file_name):
    """Carrega e aplica o CSS personalizado, forçando a codificação UTF-8."""
    if not os.path.exists(file_name):
        st.warning(f"O arquivo CSS '{file_name}' não foi encontrado.")
        return
    # Adicione encoding='utf-8' para resolver o problema de decodificação.
    with open(file_name, encoding='utf-8') as f: 
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
load_css("style.css")

st.set_page_config(page_title="Produtos Vendidos - Cores e Fragrâncias")

st.title("💰 Produtos Vendidos")

# Filtra produtos que foram vendidos (vendido = 1)
produtos_vendidos = [p for p in get_all_produtos() if p.get("vendido") == 1 and p.get("quantidade") == 0]

if not produtos_vendidos:
    st.info("Nenhum produto foi vendido e saiu totalmente do estoque ainda.")
else:
    for p in produtos_vendidos:
        st.markdown(f"### **{p.get('nome')}**")
        st.write(f"**Preço de Venda (Último):** R$ {float(p.get('preco')):.2f}")
        st.write(f"**Data da Última Venda:** {p.get('data_ultima_venda') or 'N/A'}")
        st.write(f"**Marca:** {p.get('marca')}")
        st.write(f"**Estilo:** {p.get('estilo')}")
        st.write(f"**Tipo:** {p.get('tipo')}")
        st.markdown("---")