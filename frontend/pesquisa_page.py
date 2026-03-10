import streamlit as st
from backend.database import listar_perguntas, salvar_resposta_cliente, supabase

def exibir_pesquisa():
    # Pega o ID da URL (ex: ?id=123456)
    id_pesquisa = st.query_params.get("id")
    
    if not id_pesquisa:
        st.error("⚠️ Nenhum código de pesquisa encontrado. Verifique se o link está correto.")
        return

    # Busca o nome da pesquisa na nuvem
    resposta_pesq = supabase.table("pesquisas").select("nome").eq("id", id_pesquisa).execute()
    nome_pesquisa = resposta_pesq.data[0]['nome'] if resposta_pesq.data else "Pesquisa de Satisfação"

    st.title(f"📋 {nome_pesquisa}")
    st.write("Sua opinião é muito importante para nós! Leva menos de 1 minuto.")
    st.divider()

    # Carrega as perguntas desta pesquisa direto da nuvem
    perguntas_data = listar_perguntas(id_pesquisa)
    
    if not perguntas_data:
        st.info("Nenhuma pergunta configurada para esta pesquisa no momento.")
        return

    # Cria o formulário para o cliente responder
    with st.form("form_resposta"):
        respostas_cliente = {}
        
        # Puxa o texto de cada pergunta que veio do banco
        for i, p_banco in enumerate(perguntas_data):
            texto_pergunta = p_banco['texto']
            st.write(f"**{i+1}. {texto_pergunta}**")
            nota = st.slider("Nota:", min_value=0, max_value=10, value=10, key=f"q_{i}")
            
            # Guarda a pergunta e a nota
            respostas_cliente[f"pergunta_{i+1}"] = texto_pergunta
            respostas_cliente[f"nota_{i+1}"] = nota
            st.write("---")
            
        comentario = st.text_area("📝 (Opcional) Deixe um comentário ou sugestão:")
        respostas_cliente["comentario"] = comentario

        submit = st.form_submit_button("📤 Enviar Respostas", width="stretch")
        
        if submit:
            # Envia tudo para o Supabase!
            try:
                salvar_resposta_cliente(id_pesquisa, respostas_cliente)
                st.success("🎉 Muito obrigado! Suas respostas foram salvas com sucesso.")
                st.balloons()
            except Exception as e:
                st.error(f"Houve um erro ao salvar as respostas: {e}")