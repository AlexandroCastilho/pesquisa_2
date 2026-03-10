import streamlit as st
import pandas as pd
from backend.database import (
    listar_empresas, criar_empresa, alterar_status_empresa, excluir_empresa,
    listar_usuarios, criar_usuario, alterar_status_usuario, excluir_usuario
)

def exibir_painel_admin():
    st.title("👑 Sala de Controle (SaaS)")
    st.write("Gerencie seus clientes, autorize acessos e suspenda inadimplentes.")

    tab1, tab2 = st.tabs(["🏢 Empresas Clientes", "👥 Usuários do Sistema"])

    # --- ABA 1: GERENCIAR EMPRESAS ---
    with tab1:
        with st.form("form_nova_empresa"):
            st.subheader("Cadastrar Novo Cliente")
            col_nome, col_btn = st.columns([3, 1])
            nome_emp = col_nome.text_input("Nome Fantasia ou Razão Social da Empresa")
            if col_btn.form_submit_button("➕ Salvar Empresa", use_container_width=True):
                if nome_emp:
                    criar_empresa(nome_emp)
                    st.success(f"Empresa '{nome_emp}' cadastrada com sucesso!")
                    st.rerun()

        st.divider()
        st.subheader("Base de Clientes")
        empresas = listar_empresas()
        
        if empresas:
            for emp in empresas:
                # BLINDAGEM: Usamos .get() para não travar se a coluna não vier do banco
                status_atual = emp.get('status', 'ativo')
                cor_status = "🟢 Ativa" if status_atual == 'ativo' else "🔴 Bloqueada"
                
                with st.expander(f"{emp.get('nome', 'Sem Nome')} - {cor_status}"):
                    st.write(f"**ID no Banco:** `{emp.get('id', '')}`")
                    
                    # Blindagem da data de cadastro
                    data_cad = emp.get('data_cadastro')
                    texto_data = data_cad[:10] if data_cad else "Data não registrada"
                    st.write(f"**Cliente desde:** {texto_data}")
                    
                    c1, c2 = st.columns(2)
                    novo_status = 'bloqueado' if status_atual == 'ativo' else 'ativo'
                    texto_btn = "🚫 Suspender Acesso" if status_atual == 'ativo' else "✅ Liberar Acesso"
                    
                    if c1.button(texto_btn, key=f"status_emp_{emp.get('id')}", use_container_width=True):
                        alterar_status_empresa(emp['id'], novo_status)
                        st.rerun()
                    if c2.button("🗑️ Excluir Empresa (Irreversível)", key=f"del_emp_{emp.get('id')}", use_container_width=True, type="secondary"):
                        excluir_empresa(emp['id'])
                        st.rerun()
        else:
            st.info("Nenhuma empresa cadastrada ainda.")

    # --- ABA 2: GERENCIAR USUÁRIOS ---
    with tab2:
        empresas = listar_empresas()
        if not empresas:
            st.warning("⚠️ Você precisa cadastrar uma Empresa primeiro antes de criar usuários.")
        else:
            opcoes_emp = {e['nome']: e['id'] for e in empresas if 'nome' in e and 'id' in e}
            
            with st.form("form_novo_usuario"):
                st.subheader("Criar Acesso (Login)")
                emp_selecionada = st.selectbox("Vincular este funcionário a qual empresa?", list(opcoes_emp.keys()))
                
                c1, c2, c3 = st.columns(3)
                nome_user = c1.text_input("Nome do Usuário")
                email_user = c2.text_input("E-mail de Login")
                senha_user = c3.text_input("Senha Inicial", type="password")
                
                if st.form_submit_button("➕ Criar Credencial", use_container_width=True):
                    if nome_user and email_user and senha_user:
                        criar_usuario(opcoes_emp[emp_selecionada], nome_user, email_user, senha_user)
                        st.success("Acesso liberado com sucesso!")
                        st.rerun()

            st.divider()
            st.subheader("Todos os Usuários")
            usuarios = listar_usuarios()
            
            if usuarios:
                # Cria uma tabela bonita para visualizar todo mundo
                df_users = []
                for u in usuarios:
                    nome_empresa = u.get('empresas', {}).get('nome', 'Desconhecida') if isinstance(u.get('empresas'), dict) else 'Desconhecida'
                    status_u = u.get('status', 'ativo')
                    
                    df_users.append({
                        "Nome": u.get('nome', ''),
                        "E-mail": u.get('email', ''),
                        "Empresa": nome_empresa,
                        "Status": "Ativo" if status_u == 'ativo' else "Bloqueado"
                    })
                st.dataframe(pd.DataFrame(df_users), use_container_width=True)
                
                # Botões rápidos de ação
                st.write("**Ações Rápidas de Usuário:**")
                c_sel, c_bloq, c_del = st.columns([2, 1, 1])
                email_acao = c_sel.selectbox("Selecione o E-mail para modificar:", [u.get('email') for u in usuarios], label_visibility="collapsed")
                
                user_selecionado = next((u for u in usuarios if u.get('email') == email_acao), None)
                if user_selecionado:
                    status_atual_u = user_selecionado.get('status', 'ativo')
                    novo_status_u = 'bloqueado' if status_atual_u == 'ativo' else 'ativo'
                    btn_texto_u = "🚫 Suspender" if status_atual_u == 'ativo' else "✅ Liberar"
                    
                    if c_bloq.button(btn_texto_u, use_container_width=True):
                        alterar_status_usuario(user_selecionado['id'], novo_status_u)
                        st.rerun()
                    if c_del.button("🗑️ Excluir", use_container_width=True):
                        excluir_usuario(user_selecionado['id'])
                        st.rerun()