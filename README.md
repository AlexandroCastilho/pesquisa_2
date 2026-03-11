# Sistema de Pesquisas (Streamlit + Supabase)

Aplicação SaaS para criação de pesquisas de satisfação, disparo por e-mail e dashboard de resultados.

## Funcionalidades

- Login corporativo por empresa.
- Modo super admin (gestão global de empresas e usuários).
- CRUD de pesquisas e perguntas.
- Upload de base de clientes por CSV.
- Disparo de convites por SMTP.
- Dashboard com média de notas, NPS e comentários.

## Estrutura

- `app.py`: roteamento principal da aplicação.
- `frontend/`: páginas Streamlit (login, gestão, dashboard etc).
- `backend/database.py`: acesso ao Supabase e regras principais de backend.
- `backend/email_service.py`: envio de convite por SMTP.
- `teste_conexao.py`: teste de autenticação SMTP via config de uma empresa.
- `teste_envio_real.py`: envio real de e-mail de teste.
- `ler_banco.py`: leitura de configurações SMTP salvas no Supabase.

## Requisitos

- Python 3.10+
- Conta Supabase com tabelas já provisionadas.
- Arquivo `.streamlit/secrets.toml` com credenciais.

## Secrets esperados

```toml
SUPABASE_URL = "https://...supabase.co"
SUPABASE_KEY = "..."
SUPERADMIN_EMAIL = "admin@seu-dominio.com"
SUPERADMIN_PASSWORD = "senha-forte"
```

## Instalação

```bash
pip install -r requirements.txt
```

## Execução

```bash
streamlit run app.py
```

## Scripts utilitários

### 1) Testar conexão SMTP

```bash
EMPRESA_ID=<uuid-da-empresa> python teste_conexao.py
```

### 2) Enviar e-mail real de teste

```bash
EMPRESA_ID=<uuid-da-empresa> EMAIL_DESTINO=voce@email.com python teste_envio_real.py
```

### 3) Listar configurações SMTP cadastradas

```bash
python ler_banco.py
```

## Testes

```bash
python -m unittest tests/test_security.py
```


## Observação importante

Se você estiver vendo apenas algo como:

`usuario,senha,nome ...`

isso é conteúdo legado e **não** é o README atual do projeto.
O README correto é este arquivo (`README.md`) com a documentação completa.
