import os
import smtplib
from backend.database import obter_configuracoes


def testar_conexao_smtp():
    print("--- 🔍 TESTE DE CONEXÃO SMTP (SUPABASE) ---")

    empresa_id = os.getenv("EMPRESA_ID", "")
    if not empresa_id:
        print("❌ Defina a variável de ambiente EMPRESA_ID para testar a configuração de uma empresa.")
        return

    try:
        config = obter_configuracoes(empresa_id)

        if not config or not config.get("host"):
            print("❌ ERRO: Configurações SMTP não encontradas para a empresa informada.")
            return

        host = config["host"]
        porta = int(config["porta"])
        user_smtp = config["user_smtp"]
        senha_app = config["senha_app"]

        print(f"📡 Servidor: {host} | Porta: {porta}")
        print(f"👤 Usuário: {user_smtp}")
        print("⏳ Conectando...")

        if porta == 465:
            server = smtplib.SMTP_SSL(host, porta)
        else:
            server = smtplib.SMTP(host, porta)
            server.starttls()

        server.login(user_smtp, senha_app)
        print("✨ SUCESSO! Conexão estabelecida e login aceito pelo servidor SMTP.")
        server.quit()

    except smtplib.SMTPAuthenticationError:
        print("🔥 FALHA: Erro de Autenticação. O servidor recusou usuário/senha.")
    except (ConnectionRefusedError, TimeoutError):
        print("🔥 FALHA: O servidor não respondeu. Verifique Host e Porta.")
    except Exception as e:
        print(f"🔥 ERRO TÉCNICO: {e}")


if __name__ == "__main__":
    testar_conexao_smtp()
