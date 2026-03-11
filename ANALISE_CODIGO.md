# Análise Técnica do Projeto `pesquisa_2`

## 1) Visão geral

O projeto é uma aplicação Streamlit de pesquisa de satisfação com:
- autenticação;
- gestão de pesquisas/perguntas/clientes;
- disparo de e-mails SMTP;
- dashboard de resultados;
- modo super admin multiempresa.

A arquitetura atual é simples e funcional para MVP, com separação em `frontend/` e `backend/`.

## 2) Pontos fortes

- **Fluxo principal coeso** no `app.py`: login, roteamento e permissões por perfil.
- **Integração Supabase centralizada** em `backend/database.py`.
- **Interface rica em Streamlit** com páginas de login, gestão, painel e configuração.
- **Validações básicas de sessão** em múltiplas páginas (`empresa_id` em `session_state`).

## 3) Riscos e problemas encontrados

### Segurança

1. **Senhas em texto plano no Supabase**
   - `criar_usuario` salva senha sem hash.
   - `autenticar_usuario` compara e-mail+senha diretamente no banco.

2. **Credencial hardcoded de super admin**
   - `admin@castilhos.com` e senha `1234` fixos no código.

3. **Segredos SMTP potencialmente expostos**
   - `senha_app` é persistida sem criptografia de aplicação.

### Qualidade e manutenção

4. **Scripts legados quebrados**
   - `teste_conexao.py`, `teste_envio_real.py` e `ler_banco.py` importam `obter_conexao`, função que não existe mais após migração para Supabase.

5. **README inconsistente**
   - O `README.md` contém apenas linhas de CSV e não documentação do projeto.

6. **Duplicação de tela administrativa**
   - `frontend/super_admin_page.py` e parte da lógica administrativa têm estrutura muito próxima da gestão comum; risco de divergência futura.

### Confiabilidade

7. **Ausência de tratamento de exceções em operações críticas do banco**
   - Várias funções de `database.py` assumem sucesso do Supabase sem fallback/mensagem contextual.

8. **Ausência de testes automatizados**
   - Não há suíte de testes para fluxos de autenticação, CRUD e dashboard.

## 4) Prioridade de correção (ordem sugerida)

1. **Segurança de autenticação**
   - Aplicar hash (`bcrypt`/`argon2`) no cadastro e validação por hash no login.
   - Remover credenciais hardcoded e usar variável secreta.

2. **Saneamento de scripts utilitários**
   - Atualizar scripts para Supabase ou removê-los.

3. **Observabilidade e robustez**
   - Adicionar tratamento de erro padronizado nas funções do `database.py`.

4. **Testes mínimos**
   - Cobrir autenticação, criação de pesquisa, salvamento de respostas e cálculo do dashboard.

5. **Documentação real no README**
   - Setup local, variáveis de ambiente, estrutura e fluxo de deploy.

## 5) Sugestões objetivas de curto prazo

- Criar módulo `backend/security.py` para hash/validação de senha.
- Criar `backend/services/` para separar regra de negócio de acesso ao banco.
- Versionar esquema esperado do Supabase (SQL/migrations).
- Definir convenção de status (`ativo`/`bloqueado`) com enum consistente.

## 6) Diagnóstico final

**Estado atual:** bom MVP funcional, porém com **riscos sérios de segurança e manutenção** para produção.

**Recomendação:** antes de escalar clientes, executar uma rodada focada em:
- hardening de autenticação;
- limpeza de código legado;
- testes automatizados;
- documentação operacional.
