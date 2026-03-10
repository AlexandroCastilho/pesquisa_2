import streamlit as st
from backend.database import obter_configuracoes, salvar_configuracoes

def exibir_configuracoes():
    st.title("⚙️ Configurações do Sistema")
    st.write("Configure aqui os dados de envio de e-mail (SMTP) da sua empresa.")

    # Verifica se a pessoa realmente passou pela portaria (Login)
    if 'empresa_id' not in st.session_state:
        st.error("⚠️ Erro de sessão: ID da empresa não encontrado. Faça login novamente.")
        return

    empresa_id = st.session_state['empresa_id']

    # Puxa os dados da nuvem (Supabase) referentes APENAS a essa empresa
    config_atual = obter_configuracoes(empresa_id)
    
    # Prepara os valores para preencher os campos (ou deixa em branco se for o primeiro acesso)
    host_padrao = config_atual.get('host', '') if config_atual else ''
    porta_padrao = int(config_atual.get('porta', 465)) if config_atual and config_atual.get('porta') else 465
    user_padrao = config_atual.get('user_smtp', '') if config_atual else ''
    senha_padrao = config_atual.get('senha_app', '') if config_atual else ''

    with st.form("form_config"):
        st.subheader("Servidor de E-mail (SMTP)")
        
        host = st.text_input("Host SMTP (ex: smtps.uhserver.com)", value=host_padrao)
        porta = st.number_input("Porta (ex: 465 ou 587)", value=porta_padrao, step=1)
        user_smtp = st.text_input("E-mail de Envio (ex: contato@suaempresa.com)", value=user_padrao)
        senha_app = st.text_input("Senha do E-mail", value=senha_padrao, type="password")
        
        # Substituímos o use_container_width antigo pelo novo width="stretch"
        submit = st.form_submit_button("💾 Salvar Configurações", width="stretch")
        
        if submit:
            if host and porta and user_smtp and senha_app:
                salvar_configuracoes(empresa_id, host, porta, user_smtp, senha_app)
                st.success("✅ Configurações salvas com sucesso.")
                # Removi o st.rerun() daqui para a mensagem não sumir!
            else:
                st.warning("⚠️ Por favor, preencha todos os campos antes de salvar.")