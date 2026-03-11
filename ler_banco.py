from backend.database import supabase


def ver_o_que_tem_no_banco():
    print("--- 🔍 LENDO CONFIGURAÇÕES NO SUPABASE ---")

    try:
        resposta = supabase.table("configuracoes").select("empresa_id, host, porta, user_smtp").execute()
        linhas = resposta.data

        if not linhas:
            print("📭 A tabela configuracoes está vazia.")
        else:
            print("📦 DADOS ENCONTRADOS:")
            for linha in linhas:
                print(linha)

    except Exception as e:
        print(f"🔥 Erro ao ler o Supabase: {e}")


if __name__ == "__main__":
    ver_o_que_tem_no_banco()
