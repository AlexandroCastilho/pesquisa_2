import streamlit as st
from supabase import create_client

from backend.security import hash_password, is_hashed_password, verify_password

# Inicializa a conexão com a nuvem (Supabase)
@st.cache_resource
def get_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = get_supabase()


def _nome_empresa_display(empresa: dict) -> str:
    if not isinstance(empresa, dict):
        return "Sem Nome"
    return (
        empresa.get("nome")
        or empresa.get("empresa")
        or empresa.get("nome_fantasia")
        or empresa.get("razao_social")
        or "Sem Nome"
    )


def _erro_coluna_inexistente(exc: Exception, coluna: str) -> bool:
    texto = str(exc)
    return "PGRST204" in texto and f"'{coluna}'" in texto


# ==========================================
# ⚙️ CONFIGURAÇÕES DA EMPRESA (SMTP)
# ==========================================
def obter_configuracoes(empresa_id):
    if empresa_id == "admin_master":
        return None  # O Admin não tem servidor próprio
    resposta = supabase.table("configuracoes").select("*").eq("empresa_id", empresa_id).execute()
    return resposta.data[0] if resposta.data else None


def salvar_configuracoes(empresa_id, host, porta, user_smtp, senha_app):
    if empresa_id == "admin_master":
        return
    dados = {
        "empresa_id": empresa_id,
        "host": host,
        "porta": porta,
        "user_smtp": user_smtp,
        "senha_app": senha_app,
    }
    supabase.table("configuracoes").upsert(dados, on_conflict="empresa_id").execute()


# ==========================================
# 📊 PESQUISAS E PERGUNTAS
# ==========================================
def listar_pesquisas(empresa_id):
    if empresa_id == "admin_master":
        # SUPERPODER: Admin vê as pesquisas de TODAS as empresas
        resposta = supabase.table("pesquisas").select("*").execute()
    else:
        # Cliente normal vê apenas as dele
        resposta = supabase.table("pesquisas").select("*").eq("empresa_id", empresa_id).execute()
    return resposta.data


def criar_pesquisa(id_pesquisa, empresa_id, nome):
    if empresa_id == "admin_master":
        st.error("Faça login como uma empresa cliente para criar pesquisas.")
        return
    supabase.table("pesquisas").insert({"id": id_pesquisa, "empresa_id": empresa_id, "nome": nome}).execute()


def excluir_pesquisa(id_pesquisa):
    supabase.table("pesquisas").delete().eq("id", id_pesquisa).execute()


def listar_perguntas(pesquisa_id):
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
    supabase.table("respostas").insert({"pesquisa_id": pesquisa_id, "dados_json": respostas_json}).execute()


# ==========================================
# 👥 CLIENTES (BASE DE CONTATOS)
# ==========================================
def salvar_clientes_lote(pesquisa_id, df_clientes):
    supabase.table("clientes").delete().eq("pesquisa_id", pesquisa_id).execute()
    dados = []
    for _, row in df_clientes.iterrows():
        dados.append({"pesquisa_id": pesquisa_id, "email": row["email"], "nome": row.get("nome", "Cliente")})
    if dados:
        supabase.table("clientes").insert(dados).execute()


def listar_clientes(pesquisa_id):
    resposta = supabase.table("clientes").select("*").eq("pesquisa_id", pesquisa_id).execute()
    return resposta.data


def limpar_clientes(pesquisa_id):
    supabase.table("clientes").delete().eq("pesquisa_id", pesquisa_id).execute()


# ==========================================
# 📈 PAINEL DE RESULTADOS (DASHBOARD)
# ==========================================
def listar_respostas(empresa_id):
    if empresa_id == "admin_master":
        # SUPERPODER: Admin carrega os dados de todo mundo
        pesquisas = supabase.table("pesquisas").select("id, nome").execute()
    else:
        pesquisas = supabase.table("pesquisas").select("id, nome").eq("empresa_id", empresa_id).execute()

    if not pesquisas.data:
        return []

    ids_pesquisas = [p["id"] for p in pesquisas.data]
    if not ids_pesquisas:
        return []

    respostas = supabase.table("respostas").select("*").in_("pesquisa_id", ids_pesquisas).execute()

    mapa_pesquisas = {p["id"]: p["nome"] for p in pesquisas.data}
    resultados = []
    for r in respostas.data:
        r["nome_pesquisa"] = mapa_pesquisas.get(r["pesquisa_id"], "Pesquisa Desconhecida")
        resultados.append(r)

    return resultados


# ==========================================
# 🏢 GESTÃO DE EMPRESAS E USUÁRIOS (SaaS)
# ==========================================
def listar_empresas():
    resposta = supabase.table("empresas").select("*").execute()
    empresas = resposta.data or []
    for emp in empresas:
        emp["display_nome"] = _nome_empresa_display(emp)
    return empresas


def criar_empresa(nome):
    nome = (nome or "").strip()
    if not nome:
        raise ValueError("Nome da empresa é obrigatório.")

    tentativas = [
        {"nome": nome},
        {"empresa": nome},
        {"nome_fantasia": nome},
        {"razao_social": nome},
    ]

    ultimo_erro = None
    for payload in tentativas:
        try:
            resposta = supabase.table("empresas").insert(payload).execute()
            if isinstance(resposta.data, list) and len(resposta.data) > 0:
                empresa = resposta.data[0]
                empresa["display_nome"] = _nome_empresa_display(empresa)
                return empresa
            return None
        except Exception as exc:
            ultimo_erro = exc
            if not any(_erro_coluna_inexistente(exc, col) for col in payload.keys()):
                raise

    raise RuntimeError(
        "Não foi possível cadastrar empresa: tabela 'empresas' sem coluna de nome compatível "
        "('nome', 'empresa', 'nome_fantasia' ou 'razao_social')."
    ) from ultimo_erro


def alterar_status_empresa(empresa_id, novo_status):
    supabase.table("empresas").update({"status": novo_status}).eq("id", empresa_id).execute()


def excluir_empresa(empresa_id):
    supabase.table("empresas").delete().eq("id", empresa_id).execute()


def listar_usuarios(empresa_id=None):
    if empresa_id:
        resposta = supabase.table("usuarios").select("*").eq("empresa_id", empresa_id).execute()
    else:
        # Puxa todos os usuários e junta com o nome da empresa
        resposta = supabase.table("usuarios").select("*, empresas(*)").execute()
    return resposta.data


def criar_usuario(empresa_id, nome, email, senha):
    if not nome or not email or not senha:
        raise ValueError("Nome, e-mail e senha são obrigatórios.")

    dados = {
        "empresa_id": empresa_id,
        "nome": nome,
        "email": (email or "").strip().lower(),
        "senha": hash_password(senha),
    }
    supabase.table("usuarios").insert(dados).execute()


def alterar_status_usuario(usuario_id, novo_status):
    supabase.table("usuarios").update({"status": novo_status}).eq("id", usuario_id).execute()


def excluir_usuario(usuario_id):
    supabase.table("usuarios").delete().eq("id", usuario_id).execute()


def autenticar_usuario(email, senha):
    """Verifica usuário, senha e status de conta/empresa."""
    if not email or not senha:
        return {"status": "erro", "mensagem": "E-mail e senha são obrigatórios."}

    admin_email = st.secrets.get("SUPERADMIN_EMAIL")
    admin_senha = st.secrets.get("SUPERADMIN_PASSWORD")

    if admin_email and admin_senha and email == admin_email and senha == admin_senha:
        return {"status": "sucesso", "empresa_id": "admin_master"}

    try:
        email_limpo = (email or "").strip().lower()
        resposta = supabase.table("usuarios").select("*, empresas(status)").eq("email", email_limpo).execute()

        if not resposta.data:
            return {"status": "erro", "mensagem": "E-mail ou senha incorretos."}

        usuario = resposta.data[0]
        senha_ok = verify_password(senha, usuario.get("senha", ""))
        if not senha_ok:
            return {"status": "erro", "mensagem": "E-mail ou senha incorretos."}

        # Migração automática da senha legada (texto puro) para hash.
        if usuario.get("senha") and not is_hashed_password(usuario.get("senha")):
            supabase.table("usuarios").update({"senha": hash_password(senha)}).eq("id", usuario["id"]).execute()

        if usuario.get("status") == "bloqueado":
            return {"status": "erro", "mensagem": "Seu usuário está bloqueado. Contate o suporte."}

        empresa_status = "ativo"
        if "empresas" in usuario and isinstance(usuario["empresas"], dict):
            empresa_status = usuario["empresas"].get("status", "ativo")

        if empresa_status == "bloqueado":
            return {"status": "erro", "mensagem": "O acesso da sua empresa está suspenso."}

        return {"status": "sucesso", "empresa_id": usuario["empresa_id"], "usuario_nome": usuario["nome"]}
    except Exception as e:
        return {"status": "erro", "mensagem": f"Erro de banco de dados: {str(e)}"}
