import streamlit as st
from frontend.login_page import exibir_login
from frontend.pesquisa_page import exibir_pesquisa
from frontend.dashboard_page import exibir_dashboard
from frontend.admin_page import exibir_gestao_pesquisas
from frontend.config_page import exibir_configuracoes

st.set_page_config(page_title="Sistema Castilho's", layout="wide")

if 'logado' not in st.session_state:
    st.session_state['logado'] = False

# =========================================================
# ROTEAMENTO INTELIGENTE (VERIFICA SE É UM CLIENTE)
# =========================================================
id_pesquisa = st.query_params.get("id")

if id_pesquisa:
    # Se tem "id" na URL, é um cliente! Mostra direto a pesquisa e ignora o resto.
    exibir_pesquisa()
else:
    # Se NÃO tem "id", é você tentando acessar o sistema. Segue o fluxo de Login/Admin.
    if not st.session_state['logado']:
        exibir_login()
    else:
        st.sidebar.title("Menu Principal")
        pagina = st.sidebar.radio("Navegação", ["Home", "Gerenciar Pesquisas", "Configurações"])
        
        st.sidebar.divider()
        if st.sidebar.button("Sair"):
            st.session_state['logado'] = False
            st.rerun()

        if pagina == "Home":
            exibir_dashboard()
        elif pagina == "Gerenciar Pesquisas":
            exibir_gestao_pesquisas()
        elif pagina == "Configurações":
            exibir_configuracoes()