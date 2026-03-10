import sqlite3
from backend.database import obter_conexao

def ver_o_que_tem_no_banco():
    print("--- 🔍 LENDO O BANCO DE DADOS SQLITE ---")
    
    try:
        with obter_conexao() as conn:
            cursor = conn.cursor()
            
            # Busca absolutamente tudo da tabela de configurações
            cursor.execute("SELECT * FROM configuracoes")
            linhas = cursor.fetchall()
            
            if not linhas:
                print("📭 O banco de dados está VAZIO. O site não está salvando.")
            else:
                print("📦 DADOS ENCONTRADOS NO BANCO:")
                for linha in linhas:
                    print(linha)
                    
    except Exception as e:
        print(f"🔥 Erro ao ler o banco: {e}")

if __name__ == "__main__":
    ver_o_que_tem_no_banco()