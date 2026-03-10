import streamlit as st
from supabase import create_client

# Inicializa a conexão com a nuvem (Supabase)
@st.cache_resource
def get_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = get_supabase()

# ==========================================
# ⚙️ CONFIGURAÇÕES DA EMPRESA (SMTP)
# ==========================================
def obter_configuracoes(empresa_id):
    """Busca as configurações de e-mail da empresa logada."""
    resposta = supabase.table("configuracoes").select("*").eq("empresa_id", empresa_id).execute()
    if resposta.data:
        return resposta.data[0]
    return None

def salvar_configuracoes(empresa_id, host, porta, user_smtp, senha_app):
    """Salva ou atualiza os dados de disparo de e-mail da empresa."""
    dados = {
        "empresa_id": empresa_id,
        "host": host,
        "porta": porta,
        "user_smtp": user_smtp,
        "senha_app": senha_app
    }
    # O comando 'upsert' é inteligente: se não existe, ele cria. Se existe, ele atualiza.
    supabase.table("configuracoes").upsert(dados, on_conflict="empresa_id").execute()

# ==========================================
# 📊 PESQUISAS E PERGUNTAS
# ==========================================
def listar_pesquisas(empresa_id):
    """Traz apenas as pesquisas da empresa logada."""
    resposta = supabase.table("pesquisas").select("*").eq("empresa_id", empresa_id).execute()
    return resposta.data

def criar_pesquisa(id_pesquisa, empresa_id, nome):
    """Cria uma nova pesquisa atrelada à empresa."""
    supabase.table("pesquisas").insert({"id": id_pesquisa, "empresa_id": empresa_id, "nome": nome}).execute()

def excluir_pesquisa(id_pesquisa):
    """Deleta a pesquisa (e tudo o que está atrelado a ela) da nuvem."""
    supabase.table("pesquisas").delete().eq("id", id_pesquisa).execute()

def listar_perguntas(pesquisa_id):
    """Busca as perguntas de uma pesquisa específica."""
    resposta = supabase.table("perguntas").select("*").eq("pesquisa_id", pesquisa_id).execute()
    return resposta.data

def adicionar_pergunta(pesquisa_id, texto):
    supabase.table("perguntas").insert({"pesquisa_id": pesquisa_id, "texto": texto}).execute()

def deletar_pergunta(pergunta_id):
    supabase.table("perguntas").delete().eq("id", pergunta_id).execute()
    
# ==========================================
# 📩 RESPOSTAS DOS CLIENTES
# ==========================================
def salvar_resposta_cliente(pesquisa_id, respostas_json):
    """Salva o formulário respondido pelo cliente usando formato JSON."""
    supabase.table("respostas").insert({
        "pesquisa_id": pesquisa_id,
        "dados_json": respostas_json
    }).execute()

# ==========================================
# 👥 CLIENTES (BASE DE CONTATOS)
# ==========================================
def salvar_clientes_lote(pesquisa_id, df_clientes):
    """Apaga a lista antiga e salva a nova na nuvem."""
    supabase.table("clientes").delete().eq("pesquisa_id", pesquisa_id).execute()
    
    dados = []
    for _, row in df_clientes.iterrows():
        dados.append({
            "pesquisa_id": pesquisa_id,
            "email": row['email'],
            "nome": row.get('nome', 'Cliente')
        })
    if dados:
        supabase.table("clientes").insert(dados).execute()

def listar_clientes(pesquisa_id):
    """Busca os clientes salvos na nuvem para esta pesquisa."""
    resposta = supabase.table("clientes").select("*").eq("pesquisa_id", pesquisa_id).execute()
    return resposta.data

def limpar_clientes(pesquisa_id):
    """Apaga a lista de clientes de uma pesquisa."""
    supabase.table("clientes").delete().eq("pesquisa_id", pesquisa_id).execute()

# ==========================================
# 📈 PAINEL DE RESULTADOS (DASHBOARD)
# ==========================================
def listar_respostas(empresa_id):
    """Busca todas as pesquisas da empresa e depois as respostas delas."""
    # 1. Obter todas as pesquisas da empresa
    pesquisas = supabase.table("pesquisas").select("id, nome").eq("empresa_id", empresa_id).execute()
    if not pesquisas.data:
        return []
    
    # 2. Extrair apenas os IDs das pesquisas
    ids_pesquisas = [p['id'] for p in pesquisas.data]
    if not ids_pesquisas:
        return []
        
    # 3. Obter as respostas que pertencem a esses IDs
    respostas = supabase.table("respostas").select("*").in_("pesquisa_id", ids_pesquisas).execute()
    
    # 4. Juntar o nome da pesquisa aos dados da resposta para facilitar no gráfico
    mapa_pesquisas = {p['id']: p['nome'] for p in pesquisas.data}
    resultados = []
    for r in respostas.data:
        r['nome_pesquisa'] = mapa_pesquisas.get(r['pesquisa_id'], 'Pesquisa Desconhecida')
        resultados.append(r)
        
    return resultados