import streamlit as st
import pandas as pd
import uuid
from backend.database import (
    listar_pesquisas, criar_pesquisa, excluir_pesquisa,
    listar_perguntas, adicionar_pergunta, deletar_pergunta,
    salvar_clientes_lote, listar_clientes, limpar_clientes # <-- Importamos as funções novas
)
from backend.email_service import enviar_convite_pesquisa

def exibir_gestao_pesquisas():
    st.title("📝 Gestão de Pesquisas")

    if 'empresa_id' not in st.session_state:
        st.error("Sessão expirada. Faça login novamente.")
        return
    
    empresa_id = st.session_state['empresa_id']

    if 'aba_interna' not in st.session_state:
        st.session_state.aba_interna = "lista"

    # --- TELA 1: LISTA DE PESQUISAS ---
    if st.session_state.aba_interna == "lista":
        if st.button("➕ Criar Nova Pesquisa"):
            st.session_state.aba_interna = "criar"
            st.rerun()
            
        st.subheader("Suas Pesquisas")
        pesquisas_db = listar_pesquisas(empresa_id)
        
        if pesquisas_db:
            for row in pesquisas_db:
                with st.expander(f"📋 {row['nome']}"):
                    col1, col2 = st.columns(2)
                    if col1.button("Editar / Disparar", key=f"ed_{row['id']}"):
                        st.session_state.pesquisa_ativa = row['id']
                        st.session_state.pesquisa_nome = row['nome']
                        st.session_state.aba_interna = "editar"
                        st.rerun()
                    if col2.button("Excluir", key=f"del_p_{row['id']}"):
                        excluir_pesquisa(row['id'])
                        st.rerun()
        else:
            st.info("Você ainda não criou nenhuma pesquisa.")

    # --- TELA 2: CRIAR NOVA PESQUISA ---
    elif st.session_state.aba_interna == "criar":
        st.button("⬅️ Cancelar", on_click=lambda: st.session_state.update({"aba_interna": "lista"}))
        nome_p = st.text_input("Nome da Pesquisa (ex: Satisfação de Março)")
        
        if st.button("Salvar e Definir Perguntas"):
            if nome_p:
                id_p = str(uuid.uuid4())[:8]
                criar_pesquisa(id_p, empresa_id, nome_p)
                st.session_state.pesquisa_ativa = id_p
                st.session_state.pesquisa_nome = nome_p
                st.session_state.aba_interna = "editar"
                st.rerun()

    # --- TELA 3: CONFIGURAR PESQUISA E DISPARAR ---
    elif st.session_state.aba_interna == "editar":
        st.button("⬅️ Voltar para Lista", on_click=lambda: st.session_state.update({"aba_interna": "lista"}))
        st.header(f"Configurando: {st.session_state.pesquisa_nome}")
        
        # Devolvemos as 3 abas originais!
        tab1, tab2, tab3 = st.tabs(["Perguntas", "Base de Clientes", "Disparar E-mails"])
        id_atual = st.session_state.pesquisa_ativa
        
        # --- TAB 1: PERGUNTAS ---
        with tab1:
            st.subheader("Adicionar Perguntas")
            perguntas_db = listar_perguntas(id_atual)

            nova_pergunta = st.text_input("Nova pergunta:", key="input_nova_p")
            if st.button("➕ Adicionar"):
                if nova_pergunta:
                    adicionar_pergunta(id_atual, nova_pergunta)
                    st.success("Gravada na nuvem!")
                    st.rerun()

            st.write("---")
            for idx, p in enumerate(perguntas_db):
                c1, c2 = st.columns([4, 1])
                c1.text(f"{idx+1}. {p['texto']}")
                if c2.button("🗑️", key=f"del_p_item_{p['id']}"):
                    deletar_pergunta(p['id'])
                    st.rerun()

        # --- TAB 2: CLIENTES (MEMORIZA NA NUVEM) ---
        with tab2:
            st.subheader("Base de Contatos na Nuvem")
            clientes_db = listar_clientes(id_atual)
            
            if clientes_db:
                st.success(f"✅ Já existe uma lista com {len(clientes_db)} contatos salva para esta pesquisa.")
                # Exibe a tabela puxando do Supabase
                df_salvo = pd.DataFrame(clientes_db)
                st.dataframe(df_salvo[['email', 'nome']])
                
                if st.button("Substituir Lista / Limpar"):
                    limpar_clientes(id_atual)
                    st.rerun()
            else:
                uploaded_file = st.file_uploader("Upload do CSV (colunas: email, nome)", type="csv")
                if uploaded_file:
                    df_c = pd.read_csv(uploaded_file)
                    if 'email' in df_c.columns:
                        salvar_clientes_lote(id_atual, df_c) # Salva no Supabase!
                        st.success("Lista salva na nuvem com sucesso!")
                        st.rerun()
                    else:
                        st.error("O CSV deve ter uma coluna chamada 'email'.")

        # --- TAB 3: DISPARO ---
        with tab3:
            st.subheader("🚀 Central de Disparo")
            clientes_db = listar_clientes(id_atual) # Lê direto do Supabase
            
            if not clientes_db:
                st.warning("⚠️ Você precisa subir uma lista na aba 'Base de Clientes' antes de disparar.")
            else:
                st.info(f"Pronto para enviar e-mails para {len(clientes_db)} clientes.")
                
                if st.button("Confirmar e Iniciar Envio Agora", type="primary"):
                    progresso = st.progress(0)
                    status_text = st.empty()
                    log_container = st.expander("Ver Detalhes do Envio", expanded=True)
                    
                    sucessos = 0
                    erros = 0
                    url_do_seu_sistema = "https://pesquisa2-g7kcvoyq9qmoagsqgebph2.streamlit.app/"
                    link_pesquisa = f"{url_do_seu_sistema}/?id={id_atual}"
                    
                    for i, cliente in enumerate(clientes_db):
                        email_cliente = cliente['email']
                        nome_cliente = cliente.get('nome', 'Cliente')
                        
                        status_text.text(f"Enviando para: {email_cliente}...")
                        
                        sucesso, msg = enviar_convite_pesquisa(email_cliente, nome_cliente, link_pesquisa, empresa_id)
                        
                        if sucesso:
                            sucessos += 1
                            log_container.write(f"✅ Enviado: {email_cliente}")
                        else:
                            erros += 1
                            log_container.write(f"❌ Erro ({email_cliente}): {msg}")
                        
                        progresso.progress((i + 1) / len(clientes_db))
                    
                    st.success(f"Finalizado! {sucessos} e-mails enviados, {erros} erros.")
                    if sucessos > 0:
                        st.balloons()