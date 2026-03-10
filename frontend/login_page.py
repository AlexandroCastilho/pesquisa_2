import streamlit as st
from backend.auth import verificar_login, cadastrar_usuario, validar_email

def exibir_login():
    st.markdown("<h2 style='text-align: center;'>Acesso ao Sistema</h2>", unsafe_allow_html=True)
    
    # Criando abas para Login e Cadastro
    aba_login, aba_cadastro = st.tabs(["Entrar", "Criar Conta"])

    with aba_login:
        with st.form("form_login"):
            email = st.text_input("E-mail").strip()
            senha = st.text_input("Senha", type="password")
            btn_login = st.form_submit_button("Entrar", use_container_width=True)
            
            if btn_login:
                if not email:
                    st.error("Por favor, insira seu e-mail.")
                elif not validar_email(email):
                    st.error("E-mail inválido. Verifique o formato.")
                elif not senha:
                    st.error("Por favor, insira sua senha.")
                else:
                    sucesso, nome = verificar_login(email, senha)
                    if sucesso:
                        st.session_state['logado'] = True
                        st.session_state['usuario_nome'] = nome
                        st.rerun()
                    else:
                        st.error("E-mail ou senha incorretos.")

    with aba_cadastro:
        with st.form("form_cadastro"):
            novo_nome = st.text_input("Nome Completo").strip()
            novo_email = st.text_input("E-mail de Acesso").strip()
            nova_senha = st.text_input("Crie uma Senha", type="password")
            confirmar_senha = st.text_input("Confirme a Senha", type="password")
            btn_cadastrar = st.form_submit_button("Finalizar Cadastro", use_container_width=True)

            if btn_cadastrar:
                if not novo_nome:
                    st.error("Por favor, insira seu nome completo.")
                elif not novo_email:
                    st.error("Por favor, insira seu e-mail.")
                elif not validar_email(novo_email):
                    st.error("E-mail inválido. Verifique o formato.")
                elif len(nova_senha) < 8:
                    st.warning("A senha deve ter pelo menos 8 caracteres.")
                elif nova_senha != confirmar_senha:
                    st.warning("As senhas não conferem!")
                else:
                    sucesso, msg = cadastrar_usuario(novo_nome, novo_email, nova_senha)
                    if sucesso:
                        st.success(msg)
                    else:
                        st.error(msg)