import streamlit as st
import pandas as pd
import os
import uuid

def exibir_gestao_pesquisas():
    st.title("📝 Gestão de Pesquisas")
    
    # Criar pasta de dados se não existir
    if not os.path.exists('backend/data'):
        os.makedirs('backend/data')

    if 'aba_interna' not in st.session_state:
        st.session_state.aba_interna = "lista"

    # --- TELA 1: LISTA DE PESQUISAS ---
    if st.session_state.aba_interna == "lista":
        if st.button("➕ Criar Nova Pesquisa"):
            st.session_state.aba_interna = "criar"
            st.rerun()
            
        st.subheader("Suas Pesquisas")
        caminho_pesquisas = 'backend/data/pesquisas.csv'
        
        if os.path.exists(caminho_pesquisas):
            df = pd.read_csv(caminho_pesquisas)
            for i, row in df.iterrows():
                with st.expander(f"📋 {row['nome']}"):
                    col1, col2 = st.columns(2)
                    if col1.button("Editar Perguntas/Clientes", key=f"ed_{row['id']}"):
                        st.session_state.pesquisa_ativa = row['id']
                        st.session_state.pesquisa_nome = row['nome']
                        st.session_state.aba_interna = "editar"
                        st.rerun()
                    if col2.button("Excluir", key=f"del_p_{row['id']}"):
                        df = df.drop(i)
                        df.to_csv(caminho_pesquisas, index=False)
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
                nova_p = pd.DataFrame([[id_p, nome_p]], columns=['id', 'nome'])
                caminho_pesquisas = 'backend/data/pesquisas.csv'
                
                if not os.path.exists(caminho_pesquisas):
                    nova_p.to_csv(caminho_pesquisas, index=False)
                else:
                    pd.concat([pd.read_csv(caminho_pesquisas), nova_p]).to_csv(caminho_pesquisas, index=False)
                
                st.session_state.pesquisa_ativa = id_p
                st.session_state.pesquisa_nome = nome_p
                st.session_state.aba_interna = "editar"
                st.rerun()

    # --- TELA 3: CONFIGURAR PESQUISA ESPECÍFICA (ABAS) ---
    elif st.session_state.aba_interna == "editar":
        st.button("⬅️ Voltar para Lista", on_click=lambda: st.session_state.update({"aba_interna": "lista"}))
        st.header(f"Configurando: {st.session_state.pesquisa_nome}")
        
        # AQUI É ONDE AS TABS SÃO DEFINIDAS
        tab1, tab2, tab3 = st.tabs(["Perguntas", "Clientes (CSV)", "Disparar"])
        
        # --- TAB PERGUNTAS ---
        with tab1:
            id_atual = st.session_state.pesquisa_ativa
            arq_perguntas = f'backend/data/perguntas_{id_atual}.csv'
            
            st.subheader("Adicionar Perguntas")
            
            if os.path.exists(arq_perguntas):
                df_p = pd.read_csv(arq_perguntas)
                lista_p = df_p['texto'].tolist()
            else:
                lista_p = []

            nova_pergunta = st.text_input("Nova pergunta:", key="input_nova_p")
            if st.button("➕ Adicionar"):
                if nova_pergunta:
                    lista_p.append(nova_pergunta)
                    pd.DataFrame(lista_p, columns=['texto']).to_csv(arq_perguntas, index=False)
                    st.success("Gravado!")
                    st.rerun()

            st.write("---")
            for idx, p_texto in enumerate(lista_p):
                c1, c2 = st.columns([4, 1])
                c1.text(f"{idx+1}. {p_texto}")
                if c2.button("🗑️", key=f"del_p_item_{idx}"):
                    lista_p.pop(idx)
                    pd.DataFrame(lista_p, columns=['texto']).to_csv(arq_perguntas, index=False)
                    st.rerun()

# --- TAB CLIENTES (CORRIGIDA) ---
        with tab2:
            st.subheader("Base de Contatos para esta Pesquisa")
            id_atual = st.session_state.pesquisa_ativa
            arq_clientes = f'backend/data/clientes_{id_atual}.csv'
            
            # Verificar se já existe uma lista salva
            if os.path.exists(arq_clientes):
                df_salvo = pd.read_csv(arq_clientes)
                st.success(f"✅ Já existe uma lista com {len(df_salvo)} contatos salva para esta pesquisa.")
                st.dataframe(df_salvo.head(5), use_container_width=True)
                if st.button("Substituir Lista/Limpar"):
                    os.remove(arq_clientes)
                    st.rerun()
            else:
                uploaded_file = st.file_uploader("Upload do CSV (colunas: email, nome)", type="csv")
                if uploaded_file:
                    df_c = pd.read_csv(uploaded_file)
                    if 'email' in df_c.columns:
                        df_c.to_csv(arq_clientes, index=False)
                        st.success(f"Base salva com {len(df_c)} contatos!")
                        st.rerun() # Recarrega para mostrar a tabela salva
                    else:
                        st.error("O CSV deve ter uma coluna chamada 'email'.")

# --- TAB DISPARO (COM FEEDBACK REAL) ---
        with tab3:
            st.subheader("🚀 Central de Disparo")
            id_atual = st.session_state.pesquisa_ativa
            arq_clientes = f'backend/data/clientes_{id_atual}.csv'
            
            if not os.path.exists(arq_clientes):
                st.warning("⚠️ Você precisa subir uma lista de clientes na aba ao lado antes de disparar.")
            else:
                df_para_envio = pd.read_csv(arq_clientes)
                st.info(f"Pronto para enviar para {len(df_para_envio)} contatos.")
                
                if st.button("Confirmar e Iniciar Envio Agora"):
                    progresso = st.progress(0)
                    status_text = st.empty()
                    log_container = st.expander("Ver Detalhes do Envio", expanded=True)
                    
                    sucessos = 0
                    erros = 0
                    
                    for i, row in df_para_envio.iterrows():
                        status_text.text(f"Enviando para: {row['email']}...")
                        
                        # Chama a função de e-mail (ajuste conforme seu email_service.py)
                        # Aqui simulamos o sucesso, mas você deve usar sua função real:
                        # sucesso, msg = enviar_convite_pesquisa(row['email'], row.get('nome', 'Cliente'))
                        sucesso = True # Simulação para teste
                        
                        if sucesso:
                            sucessos += 1
                            log_container.write(f"✅ Enviado: {row['email']}")
                        else:
                            erros += 1
                            log_container.write(f"❌ Erro: {row['email']}")
                        
                        # Atualiza barra de progresso
                        progresso.progress((i + 1) / len(df_para_envio))
                    
                    st.success(f"Finalizado! {sucessos} e-mails enviados, {erros} erros.")
                    st.balloons()