import streamlit as st
import pandas as pd
import os

CAMINHO_CONFIG = 'backend/data/config_geral.csv'

def exibir_configuracoes():
    st.title("⚙️ Configurações do Sistema")
    
    # Carregar dados existentes para preencher os campos automaticamente
    if os.path.exists(CAMINHO_CONFIG):
        df_config = pd.read_csv(CAMINHO_CONFIG)
        # Usamos .get() ou verificação para evitar erro se a coluna não existir ainda
        conf_empresa = df_config.iloc[0].get('empresa', "Castilho's")
        conf_email_contato = df_config.iloc[0].get('email_contato', "")
        conf_host = df_config.iloc[0].get('host', "smtp.gmail.com")
        conf_porta = int(df_config.iloc[0].get('porta', 465))
        conf_user_smtp = df_config.iloc[0].get('user_smtp', "")
        conf_senha_app = df_config.iloc[0].get('senha_app', "")
    else:
        conf_empresa, conf_email_contato = "Castilho's", ""
        conf_host, conf_porta = "smtp.gmail.com", 465
        conf_user_smtp, conf_senha_app = "", ""

    with st.form("form_config_geral"):
        st.subheader("👤 Perfil e ✉️ Servidor de E-mail")
        
        col1, col2 = st.columns(2)
        with col1:
            empresa = st.text_input("Nome da Empresa", value=conf_empresa)
            email_c = st.text_input("E-mail de Contato", value=conf_email_contato)
        
        with col2:
            host = st.text_input("Host SMTP (ex: smtp.gmail.com)", value=conf_host)
            porta = st.number_input("Porta SMTP (Geralmente 465 ou 587)", value=conf_porta)
            
        user_smtp = st.text_input("E-mail de Envio (Remetente)", value=conf_user_smtp)
        senha_app = st.text_input("Senha de App (SMTP)", value=conf_senha_app, type="password")
        
        if st.form_submit_button("Salvar Todas as Configurações"):
            dados = {
                'empresa': [empresa],
                'email_contato': [email_c],
                'host': [host],
                'porta': [porta],
                'user_smtp': [user_smtp],
                'senha_app': [senha_app]
            }
            pd.DataFrame(dados).to_csv(CAMINHO_CONFIG, index=False)
            st.success("✅ Configurações salvas com sucesso!")
            st.rerun()