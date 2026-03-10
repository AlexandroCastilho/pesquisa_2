import streamlit as st
from frontend.login_page import exibir_login
from frontend.pesquisa_page import exibir_pesquisa
from frontend.dashboard_page import exibir_dashboard
from frontend.admin_page import exibir_gestao_pesquisas
from frontend.config_page import exibir_configuracoes
from frontend.super_admin_page import exibir_painel_admin # Puxamos a sua sala secreta!

st.set_page_config(page_title="Sistema de Pesquisas", layout="wide")

if 'logado' not in st.session_state:
    st.session_state['logado'] = False

id_pesquisa = st.query_params.get("id")

if id_pesquisa:
    exibir_pesquisa()
else:
    if not st.session_state['logado']:
        exibir_login()
    else:
        st.sidebar.title("Navegação")
        
        # MENU INTELIGENTE: Muda dependendo de quem logou!
        if st.session_state['empresa_id'] == "admin_master":
            st.sidebar.markdown("👑 **Modo Super Admin**")
            opcoes_menu = ["Painel SaaS (Clientes)", "Dashboard Global", "Gerenciar Pesquisas", "Configurações"]
        else:
            nome_usuario = st.session_state.get('usuario_nome', 'Usuário')
            st.sidebar.markdown(f"👤 **Olá, {nome_usuario}**")
            opcoes_menu = ["Home", "Gerenciar Pesquisas", "Configurações"]

        pagina = st.sidebar.radio("Selecione:", opcoes_menu)
        
        st.sidebar.divider()
        if st.sidebar.button("Sair / Logout"):
            st.session_state['logado'] = False
            st.rerun()

        # Encaminha o usuário para a tela certa
        if pagina == "Painel SaaS (Clientes)":
            exibir_painel_admin()
        elif pagina in ["Home", "Dashboard Global"]:
            exibir_dashboard()
        elif pagina == "Gerenciar Pesquisas":
            exibir_gestao_pesquisas()
        elif pagina == "Configurações":
            exibir_configuracoes()