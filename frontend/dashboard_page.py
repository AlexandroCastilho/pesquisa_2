import streamlit as st
import pandas as pd
from backend.database import listar_respostas

def exibir_dashboard():
    st.title("📊 Painel de Resultados")
    
    if 'empresa_id' not in st.session_state:
        st.error("Sessão expirada. Por favor, inicie sessão novamente.")
        return
        
    empresa_id = st.session_state['empresa_id']
    
    # Puxa todas as respostas da nuvem
    respostas = listar_respostas(empresa_id)
    
    if not respostas:
        st.info("Ainda não existem respostas para as suas pesquisas. Dispare os convites e aguarde!")
        return
        
    # Processar os dados (que estão em formato JSON na base de dados)
    dados_processados = []
    comentarios = []
    
    for r in respostas:
        json_data = r['dados_json']
        data_formatada = r['data_hora'][:10] # Pega apenas a data YYYY-MM-DD
        
        # Extrair notas das perguntas
        for chave, valor in json_data.items():
            if chave.startswith("nota_"):
                num_pergunta = chave.split("_")[1]
                pergunta_texto = json_data.get(f"pergunta_{num_pergunta}", f"Pergunta {num_pergunta}")
                dados_processados.append({
                    "Pesquisa": r['nome_pesquisa'],
                    "Data": data_formatada,
                    "Pergunta": pergunta_texto,
                    "Nota": int(valor)
                })
                
        # Extrair comentários (se houver)
        if json_data.get('comentario'):
            comentarios.append({
                "Pesquisa": r['nome_pesquisa'],
                "Data": data_formatada,
                "Comentário": json_data['comentario']
            })

    if not dados_processados:
        st.warning("Respostas encontradas, mas sem notas computáveis.")
        return

    df = pd.DataFrame(dados_processados)
    
    # --- MÉTRICAS DE TOPO ---
    st.subheader("Visão Geral do Negócio")
    col1, col2, col3 = st.columns(3)
    
    total_respostas = len(respostas)
    media_geral = df['Nota'].mean()
    
    # Cálculo NPS (Promotores: notas 9 e 10 | Detratores: notas 0 a 6)
    promotores = len(df[df['Nota'] >= 9])
    detratores = len(df[df['Nota'] <= 6])
    total_notas = len(df)
    nps = ((promotores - detratores) / total_notas) * 100 if total_notas > 0 else 0
    
    col1.metric("Total de Questionários Respondidos", total_respostas)
    col2.metric("Média Geral de Satisfação", f"{media_geral:.1f} / 10")
    col3.metric("NPS (Net Promoter Score)", f"{nps:.0f}")
    
    st.divider()
    
    # --- GRÁFICOS VISUAIS ---
    col_grafico1, col_grafico2 = st.columns(2)
    
    with col_grafico1:
        st.subheader("Média de Notas por Pesquisa")
        media_por_pesquisa = df.groupby('Pesquisa')['Nota'].mean().reset_index()
        st.bar_chart(data=media_por_pesquisa, x='Pesquisa', y='Nota')
        
    with col_grafico2:
        st.subheader("Distribuição de Notas (Geral)")
        distribuicao = df['Nota'].value_counts().sort_index().reset_index()
        distribuicao.columns = ['Nota', 'Quantidade']
        st.bar_chart(data=distribuicao, x='Nota', y='Quantidade')

    # --- ZONA DE COMENTÁRIOS ---
    st.divider()
    st.subheader("📝 Comentários e Sugestões dos Clientes")
    
    if comentarios:
        df_comentarios = pd.DataFrame(comentarios)
        st.dataframe(df_comentarios)
    else:
        st.write("Nenhum comentário deixado até ao momento.")