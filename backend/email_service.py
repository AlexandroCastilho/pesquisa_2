import smtplib
from email.message import EmailMessage
import pandas as pd
import os
import time

def enviar_convite_pesquisa(destinatario, nome_cliente, link_pesquisa):
    """
    Lê as configurações do config_geral.csv e dispara um e-mail individual.
    Valida entrada e trata erros de forma robusta.
    """
    caminho_config = 'backend/data/config_geral.csv'
    
    # Validação de entrada
    if not destinatario or not nome_cliente or not link_pesquisa:
        return False, "Erro: Dados de e-mail incompletos."
    
    # 1. Verifica se as configurações existem
    if not os.path.exists(caminho_config):
        return False, "Erro: Configure o SMTP na página de Configurações primeiro."
    
    try:
        # 2. Carrega os dados do CSV
        df = pd.read_csv(caminho_config)
        if df.empty:
            return False, "Erro: Arquivo de configuração está vazio."
        
        if len(df.columns) < 5:
            return False, "Erro: Arquivo de configuração incompleto."
            
        cfg = df.iloc[0]
        
        # Extrai variáveis com segurança e validação de tipo
        try:
            host = str(cfg['host']).strip()
            porta = int(cfg['porta'])
            user_smtp = str(cfg['user_smtp']).strip()
            senha_app = str(cfg['senha_app']).strip()
            empresa = str(cfg['empresa']).strip()
        except (ValueError, KeyError) as e:
            return False, f"Erro: Campo obrigatório faltando ou inválido ({str(e)})"
        
        # Validação de valores
        if not host or not user_smtp or not senha_app:
            return False, "Erro: Configurações SMTP incompletas."
        
        if porta not in [465, 587]:
            return False, "Erro: Porta SMTP deve ser 465 (SSL) ou 587 (TLS)."

        # 3. Monta o e-mail
        msg = EmailMessage()
        msg['Subject'] = f"Sua opinião é importante para a {empresa}!"
        msg['From'] = user_smtp
        msg['To'] = destinatario
        
        corpo = f"""
Olá, {nome_cliente}!

Gostaríamos de saber como foi sua última experiência conosco na {empresa}.
Sua avaliação nos ajuda a melhorar cada vez mais.

Para responder, basta clicar no link abaixo:
{link_pesquisa}

Atenciosamente,
Equipe {empresa}
        """
        msg.set_content(corpo)

        # 4. Lógica de Conexão SMTP (Diferencia SSL de TLS)
        try:
            if porta == 465:
                # Conexão SSL Direta (Comum no Gmail porta 465)
                with smtplib.SMTP_SSL(host, porta, timeout=10) as server:
                    server.login(user_smtp, senha_app)
                    server.send_message(msg)
            else:
                # Conexão STARTTLS (Comum na porta 587)
                with smtplib.SMTP(host, porta, timeout=10) as server:
                    server.starttls()  # Inicia a criptografia
                    server.login(user_smtp, senha_app)
                    server.send_message(msg)
            
            return True, "E-mail enviado com sucesso!"
        
        except smtplib.SMTPAuthenticationError:
            return False, "Erro: Credenciais SMTP inválidas (usuário ou senha)."
        except smtplib.SMTPException as e:
            return False, f"Erro SMTP: {str(e)}"
        except TimeoutError:
            return False, "Erro: Timeout na conexão com servidor SMTP."

    except FileNotFoundError:
        return False, "Erro: Arquivo de configuração não encontrado."
    except pd.errors.EmptyDataError:
        return False, "Erro: Arquivo de configuração vazio."
    except Exception as e:
        # Retorna o erro exato para aparecer na tela do Admin
        return False, f"Falha ao enviar e-mail: {str(e)}"