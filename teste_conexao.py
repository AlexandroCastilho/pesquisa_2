import smtplib
from backend.database import obter_conexao

def testar_conexao_smtp():
    print("--- 🔍 TESTE DE CONEXÃO SMTP (WEBMAIL) ---")
    
    try:
        # Puxando a conexão oficial do nosso backend
        with obter_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT host, porta, user_smtp, senha_app FROM configuracoes WHERE id = 1")
            resultado = cursor.fetchone()

        if not resultado or not resultado[0]:
            print("❌ ERRO: Configurações vazias. Vá no site, preencha os dados e clique em 'Salvar Configurações no Banco'.")
            return

        host, porta, user_smtp, senha_app = resultado
        porta = int(porta)

        print(f"📡 Servidor: {host} | Porta: {porta}")
        print(f"👤 Usuário: {user_smtp}")
        print("⏳ Conectando...")

        # Tentativa de Conexão e Login
        if porta == 465:
            server = smtplib.SMTP_SSL(host, porta)
        else:
            server = smtplib.SMTP(host, porta)
            server.starttls()

        server.login(user_smtp, senha_app)
        
        print("✨ SUCESSO! Conexão estabelecida e login aceito pelo Webmail.")
        server.quit()

    except smtplib.SMTPAuthenticationError:
        print("🔥 FALHA: Erro de Autenticação. O servidor recusou sua senha ou usuário.")
    except (ConnectionRefusedError, TimeoutError):
        print("🔥 FALHA: O servidor não respondeu. Verifique se o Host e a Porta estão corretos.")
    except Exception as e:
        print(f"🔥 ERRO TÉCNICO: {e}")

if __name__ == "__main__":
    testar_conexao_smtp()