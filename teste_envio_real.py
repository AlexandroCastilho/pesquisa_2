import os
import smtplib
from email.message import EmailMessage
from backend.database import obter_configuracoes


def testar_envio_real():
    print("--- 🚀 TESTE DE DISPARO REAL DE E-MAIL (SUPABASE) ---")

    empresa_id = os.getenv("EMPRESA_ID", "")
    email_destino = os.getenv("EMAIL_DESTINO", "")

    if not empresa_id or not email_destino:
        print("❌ Defina EMPRESA_ID e EMAIL_DESTINO antes de executar este teste.")
        return

    try:
        config = obter_configuracoes(empresa_id)
    except Exception as e:
        print(f"🔥 Erro ao ler configurações no Supabase: {e}")
        return

    if not config:
        print("❌ ERRO: Configurações SMTP vazias para a empresa informada.")
        return

    host = config["host"]
    porta = int(config["porta"])
    user_smtp = config["user_smtp"]
    senha_app = config["senha_app"]

    msg = EmailMessage()
    msg["Subject"] = f"Teste de Integração SaaS - Empresa {empresa_id}"
    msg["From"] = f"Sistema de Pesquisas <{user_smtp}>"
    msg["To"] = email_destino
    msg.set_content(
        "Olá!\n\n"
        "Se você recebeu esta mensagem, o teste de envio SMTP via configurações no Supabase funcionou.\n\n"
        "Abraço!"
    )

    print(f"⏳ Conectando no SMTP e enviando para {email_destino}...")

    try:
        if porta == 465:
            server = smtplib.SMTP_SSL(host, porta)
        else:
            server = smtplib.SMTP(host, porta)
            server.starttls()

        server.login(user_smtp, senha_app)
        server.send_message(msg)
        server.quit()

        print("✨ SUCESSO ABSOLUTO! O e-mail foi enviado.")
    except Exception as e:
        print(f"🔥 FALHA AO ENVIAR: {e}")


if __name__ == "__main__":
    testar_envio_real()
