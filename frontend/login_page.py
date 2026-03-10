import streamlit as st
from supabase import create_client
import uuid

# Conecta ao Supabase usando os segredos
@st.cache_resource
def init_supabase():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

supabase = init_supabase()

def exibir_login():
    st.title("🔐 Acesso ao Sistema Castilho's")
    st.write("Bem-vindo ao portal de Gestão de Pesquisas.")
    
    # Criamos abas para Login e para Cadastrar nova Empresa (para você vender)
    aba1, aba2 = st.tabs(["Entrar", "Cadastrar Nova Empresa"])
    
    with aba1:
        with st.form("form_login"):
            email_login = st.text_input("E-mail da Empresa")
            senha_login = st.text_input("Senha", type="password")
            btn_login = st.form_submit_button("Entrar", use_container_width=True) # ou width='stretch'
            
            if btn_login:
                # 1. Vai no Supabase e procura a empresa por esse e-mail (usamos o campo nome_fantasia como email provisório para login simples, ou podemos usar Auth real)
                # Para simplificar agora, vamos checar se o email está na tabela de configuracoes
                resposta = supabase.table("configuracoes").select("empresa_id, user_smtp").eq("user_smtp", email_login).execute()
                
                # NOTA: O ideal será termos uma tabela 'usuarios', mas como o Supabase tem o Auth, 
                # vamos usar uma simulação simples até você dominar o Supabase Auth.
                if len(resposta.data) > 0 or (email_login == "admin@castilhos.com" and senha_login == "1234"):
                    st.session_state['logado'] = True
                    # Se for o admin mestre, damos um ID fictício. Se for cliente, pegamos o ID dele.
                    if email_login == "admin@castilhos.com":
                        st.session_state['empresa_id'] = "admin_master"
                    else:
                        st.session_state['empresa_id'] = resposta.data[0]['empresa_id']
                        
                    st.success("Login efetuado com sucesso!")
                    st.rerun()
                else:
                    st.error("E-mail ou senha incorretos, ou empresa não cadastrada.")

    with aba2:
        st.info("Área exclusiva para cadastro de novos clientes (Venda do SaaS).")
        with st.form("form_cadastro"):
            nome_empresa = st.text_input("Nome da Empresa (ex: Amafil)")
            email_admin = st.text_input("E-mail do Administrador (Login)")
            
            btn_cadastrar = st.form_submit_button("Criar Conta e Liberar Acesso")
            
            if btn_cadastrar:
                if nome_empresa and email_admin:
                    # 1. Cria a empresa nova no Supabase
                    nova_empresa = supabase.table("empresas").insert({"nome_fantasia": nome_empresa}).execute()
                    id_nova_empresa = nova_empresa.data[0]['id']
                    
                    # 2. Cria a linha de configurações zerada para essa empresa, usando o email de admin como login
                    supabase.table("configuracoes").insert({
                        "empresa_id": id_nova_empresa,
                        "user_smtp": email_admin, # Usando como referência de login por enquanto
                    }).execute()
                    
                    st.success(f"✅ Empresa {nome_empresa} cadastrada! Ela já pode fazer login usando o e-mail: {email_admin}")
                else:
                    st.warning("Preencha todos os campos.")