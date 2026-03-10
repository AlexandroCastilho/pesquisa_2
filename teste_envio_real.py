import smtplib
from email.message import EmailMessage
from backend.database import obter_conexao

def testar_envio_real():
    print("--- 🚀 TESTE DE DISPARO REAL DE E-MAIL ---")
    
    # 1. Puxa as configurações do SQLite
    try:
        with obter_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT empresa, host, porta, user_smtp, senha_app FROM configuracoes WHERE id = 1")
            resultado = cursor.fetchone()
    except Exception as e:
        print(f"🔥 Erro ao ler o banco: {e}")
        return

    if not resultado:
        print("❌ ERRO: Configurações vazias no banco.")
        return

    empresa, host, porta, user_smtp, senha_app = resultado
    
    # ==========================================
    # 🎯 COLOQUE SEU E-MAIL PESSOAL ABAIXO
    # ==========================================
    email_destino = "alexmachado1607@gmail.com" # <-- MUDE AQUI PARA RECEBER O TESTE
    
    # 2. Monta a mensagem
    msg = EmailMessage()
    msg['Subject'] = f"Teste de Integração SaaS - {empresa}"
    msg['From'] = f"{empresa} <{user_smtp}>"
    msg['To'] = email_destino
    msg.set_content(f"Olá!\n\nSe você está lendo isso, significa que o backend do sistema da {empresa} conseguiu ler o banco SQLite e enviar este e-mail com sucesso através do UOL Host.\n\nO SaaS está ganhando vida!")

    print(f"⏳ Conectando no UOL Host e enviando para {email_destino}...")

    # 3. Dispara pela rede
    try:
        porta = int(porta)
        if porta == 465:
            server = smtplib.SMTP_SSL(host, porta)
        else:
            server = smtplib.SMTP(host, porta)
            server.starttls()
            
        server.login(user_smtp, senha_app)
        server.send_message(msg)
        server.quit()
        
        print("✨ SUCESSO ABSOLUTO! O e-mail foi despachado para a rede.")
        print(f"👉 Vá conferir a caixa de entrada (e a pasta de Spam) do e-mail: {email_destino}")
        
    except Exception as e:
        print(f"🔥 FALHA AO ENVIAR: {e}")

if __name__ == "__main__":
    testar_envio_real()