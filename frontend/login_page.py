import streamlit as st
from backend.database import autenticar_usuario # <-- Trocamos o import aqui!

def exibir_login():
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        [data-testid="stForm"] {
            background-color: var(--secondary-background-color);
            padding: 2.5rem 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border: 1px solid rgba(128,128,128,0.2);
        }
        </style>
    """, unsafe_allow_html=True)

    col_vazia_esq, col_centro, col_vazia_dir = st.columns([1, 1.2, 1])

    with col_centro:
        st.write("<br><br><br>", unsafe_allow_html=True)
        with st.form("login_form", clear_on_submit=False):
            st.markdown("<h2 style='text-align: center; color: var(--text-color); margin-bottom: 5px; font-family: sans-serif;'>Acesso Corporativo</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: var(--faded-text-color); font-size: 14px; margin-bottom: 25px; font-family: sans-serif;'>Portal de Gestão de Pesquisas</p>", unsafe_allow_html=True)
            
            email_digitado = st.text_input("E-mail corporativo", placeholder="ex: admin@castilhos.com")
            senha_digitada = st.text_input("Senha de acesso", type="password", placeholder="••••••••")
            
            st.write("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("Entrar no Sistema", use_container_width=True, type="primary")
            
            if submit:
                # AGORA USAMOS O NOVO MOTOR DE AUTENTICAÇÃO
                resultado = autenticar_usuario(email_digitado, senha_digitada)
                
                if resultado["status"] == "sucesso":
                    st.session_state['logado'] = True
                    st.session_state['empresa_id'] = resultado["empresa_id"]
                    if "usuario_nome" in resultado:
                        st.session_state['usuario_nome'] = resultado["usuario_nome"] # Guarda o nome para dar oi!
                    st.rerun()
                else:
                    st.error(resultado["mensagem"]) # Mostra se está bloqueado ou senha errada