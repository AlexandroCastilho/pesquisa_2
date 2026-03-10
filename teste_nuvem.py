import streamlit as st
from supabase import create_client

def testar_supabase():
    print("--- 🚀 A TESTAR LIGAÇÃO AO SUPABASE ---")
    try:
        # Puxa as chaves do cofre do Streamlit
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        
        # Estabelece a ligação
        print("A tentar ligar à nuvem...")
        supabase = create_client(url, key)
        
        # Tenta ler a tabela 'empresas' que criámos no passo anterior
        resposta = supabase.table("empresas").select("*").execute()
        
        print("✨ SUCESSO ABSOLUTO! O seu Python está ligado ao Supabase.")
        print(f"Empresas na base de dados: {resposta.data}")
        
    except FileNotFoundError:
        print("❌ ERRO: O ficheiro .streamlit/secrets.toml não foi encontrado.")
    except KeyError:
        print("❌ ERRO: As variáveis SUPABASE_URL ou SUPABASE_KEY não estão no ficheiro secrets.toml.")
    except Exception as e:
        print(f"🔥 ERRO TÉCNICO: {e}")

if __name__ == "__main__":
    testar_supabase()