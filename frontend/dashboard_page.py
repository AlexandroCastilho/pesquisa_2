import streamlit as st
import os
import pandas as pd

def exibir_dashboard(): # Mantendo o nome para o app.py encontrar
    st.title("🏠 Home - Painel de Controle")
    
    # Métricas de resumo
    col1, col2, col3 = st.columns(3)
    
    total_pesquisas = 0
    if os.path.exists('backend/data/pesquisas.csv'):
        df_p = pd.read_csv('backend/data/pesquisas.csv')
        total_pesquisas = len(df_p)

    col1.metric("Pesquisas Criadas", total_pesquisas)
    col2.metric("Status", "Operacional")
    col3.metric("Respostas Totais", "0")

    st.divider()
    st.subheader("Resumo de Atividade")
    st.info("Bem-vindo ao sistema da Castilho's. Use o menu lateral para gerenciar suas pesquisas.")