import smtplib
from email.message import EmailMessage
# 1. Trocamos o import antigo pelo novo comando da nuvem:
from backend.database import obter_configuracoes

# 2. Agora a função precisa saber QUAL empresa (empresa_id) está mandando o e-mail
def enviar_convite_pesquisa(destinatario, nome_cliente, link_pesquisa, empresa_id):
    try:
        # Busca os dados no Supabase protegidos pelo ID da empresa
        config = obter_configuracoes(empresa_id)

        if not config or not config.get('host'):
            return False, "Configurações de e-mail não encontradas na nuvem. Vá em Configurações e salve os dados."

        host = config['host']
        porta = int(config['porta'])
        user_smtp = config['user_smtp']
        senha_app = config['senha_app']

        # Monta o E-mail
        msg = EmailMessage()
        msg['Subject'] = "Sua opinião é muito importante para nós!"
        msg['From'] = f"Pesquisa de Satisfação <{user_smtp}>"
        msg['To'] = destinatario

        corpo_email = f"""Olá, {nome_cliente}!

Gostaríamos muito de saber sua opinião sobre a sua experiência.
Por favor, reserve um minuto para responder à nossa rápida pesquisa de satisfação clicando no link abaixo:

{link_pesquisa}

Agradecemos imensamente a sua colaboração!"""

        msg.set_content(corpo_email)

        # Conecta no servidor SMTP (UOL Host) e dispara
        if porta == 465:
            with smtplib.SMTP_SSL(host, porta) as server:
                server.login(user_smtp, senha_app)
                server.send_message(msg)
        else:
            with smtplib.SMTP(host, porta) as server:
                server.starttls()
                server.login(user_smtp, senha_app)
                server.send_message(msg)

        return True, "✨ E-mail enviado com sucesso!"

    except smtplib.SMTPAuthenticationError:
        return False, "Falha de Autenticação: Usuário ou senha incorretos."
    except Exception as e:
        return False, f"Erro no servidor de e-mail: {str(e)}"