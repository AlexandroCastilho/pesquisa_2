import streamlit as st
from backend.database import carregar_config_perguntas, salvar_pesquisa

def exibir_pesquisa():
    st.title("📊 Pesquisa de Satisfação")
    perguntas = carregar_config_perguntas()
    
    respostas = {}
    with st.form("form_dinamico"):
        respostas['cliente'] = st.text_input("Seu Nome")
        
        for p in perguntas:
            # Se a pergunta contiver "nota", usamos o slider, senão texto livre
            if "nota" in p.lower():
                respostas[p] = st.slider(p, 0, 10, 5)
            else:
                respostas[p] = st.text_area(p)
        
        if st.form_submit_button("Enviar"):
            if salvar_pesquisa(respostas):
                st.success("Enviado!")
                st.balloons()