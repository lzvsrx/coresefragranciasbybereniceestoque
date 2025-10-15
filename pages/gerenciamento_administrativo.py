import streamlit as st
from utils.database import add_user, get_user, get_all_users, hash_password
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

# Aplica o tema
load_css("style.css")

st.set_page_config(page_title="Área Administrativa - Cores e Fragrâncias")

st.title("🔐 Área Administrativa")

st.markdown("Faça login ou cadastre um novo administrador ou funcionário abaixo.")

option = st.selectbox("Escolha uma ação", ["Login", "Cadastrar Novo Usuário", "Gerenciar Contas (Admins)"])

if option == "Login":
    username = st.text_input("Nome de usuário", key="login_user")
    password = st.text_input("Senha", type="password", key="login_pass")
    if st.button("Entrar"):
        user = get_user(username)
        if not user:
            st.error("Usuário não encontrado.")
        else:
            if hash_password(password) == user.get("password"):
                st.success(f"Bem-vindo(a), {username} ({user.get('role')})!")
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["role"] = user.get('role')
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

elif option == "Cadastrar Novo Usuário":
    new_username = st.text_input("Novo nome de usuário", key="reg_user")
    new_password = st.text_input("Senha", type="password", key="reg_pass")
    confirm = st.text_input("Confirme a senha", type="password", key="reg_conf")
    role = st.selectbox("Papel do usuário", ["admin", "staff"])
    if st.button("Cadastrar"):
        if not new_username or not new_password:
            st.error("Preencha todos os campos.")
        elif new_password != confirm:
            st.error("As senhas não coincidem.")
        else:
            if get_user(new_username):
                st.error("Nome de usuário já existe.")
            else:
                add_user(new_username, new_password, role=role)
                st.success(f"Usuário '{new_username}' criado com papel '{role}'. Agora faça login.")

elif option == "Gerenciar Contas (Admins)":
    # only admin can manage
    if not st.session_state.get('logged_in') or st.session_state.get('role') != 'admin':
        st.error('Apenas administradores podem gerenciar contas. Faça login como admin.')
    else:
        st.subheader('Usuários cadastrados')
        users = get_all_users()
        for u in users:
            st.write(f"- {u.get('username')} ({u.get('role')})")