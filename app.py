import streamlit as st
from frontend.login_page import exibir_login
from frontend.pesquisa_page import exibir_pesquisa
from frontend.dashboard_page import exibir_dashboard
from frontend.admin_page import exibir_gestao_pesquisas # Alterado o nome aqui
from frontend.config_page import exibir_configuracoes

st.set_page_config(page_title="Sistema Castilho's", layout="wide")

if 'logado' not in st.session_state:
    st.session_state['logado'] = False

if not st.session_state['logado']:
    exibir_login()
else:
    # --- BARRA LATERAL ---
    st.sidebar.title("Menu Principal")
    
    # Nova organização do Menu Lateral
    pagina = st.sidebar.radio(
        "Ir para:", 
        ["Home", "Gerenciar Pesquisas", "Configurações"]
    )
    
    st.sidebar.divider()
    if st.sidebar.button("Sair"):
        st.session_state['logado'] = False
        st.rerun()

    # --- NAVEGAÇÃO ---
    if pagina == "Home":
        exibir_dashboard() # Esta é a sua Home
    elif pagina == "Gerenciar Pesquisas":
        exibir_gestao_pesquisas() # Aquela tela com o botão "Adicionar Nova"
    elif pagina == "Configurações":
        exibir_configuracoes()