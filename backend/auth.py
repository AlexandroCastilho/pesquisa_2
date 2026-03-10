import pandas as pd
import os
from werkzeug.security import generate_password_hash, check_password_hash
import re

def validar_email(email):
    """Valida o formato de um email."""
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(padrao, email) is not None

def verificar_login(email_digitado, senha_digitada):
    """Verifica credenciais de login com segurança."""
    caminho_csv = os.path.join('backend', 'data', 'usuarios.csv')
    
    # Validação de entrada
    if not email_digitado or not senha_digitada:
        return False, None
    
    if not validar_email(email_digitado):
        return False, None
    
    try:
        if not os.path.exists(caminho_csv):
            return False, None
            
        df = pd.read_csv(caminho_csv)
        
        if df.empty:
            return False, None
        
        # Procura o usuário por email
        usuario_valido = df[df['email'] == email_digitado]
        
        if usuario_valido.empty:
            return False, None
        
        # Verifica a senha usando hash seguro
        senha_hash = usuario_valido.iloc[0]['senha']
        if check_password_hash(senha_hash, senha_digitada):
            return True, usuario_valido.iloc[0]['nome']
        
        return False, None
        
    except FileNotFoundError:
        return False, None
    except Exception as e:
        print(f"Erro ao verificar login: {e}")
        return False, None

def cadastrar_usuario(nome, email, senha):
    """Cadastra um novo usuário com validações de segurança."""
    caminho_csv = os.path.join('backend', 'data', 'usuarios.csv')
    
    # Validações de entrada
    if not nome or not email or not senha:
        return False, "Preencha todos os campos."
    
    if not validar_email(email):
        return False, "E-mail inválido. Verifique o formato."
    
    if len(senha) < 8:
        return False, "A senha deve ter pelo menos 8 caracteres."
    
    try:
        if not os.path.exists(caminho_csv):
            return False, "Arquivo de dados não encontrado."
        
        df = pd.read_csv(caminho_csv)
        
        # Verifica se o e-mail já existe
        if email in df['email'].values:
            return False, "Este e-mail já está cadastrado."
        
        # Encripta a senha antes de salvar
        senha_hash = generate_password_hash(senha, method='pbkdf2:sha256')
        
        # Adiciona o novo usuário
        novo_usuario = pd.DataFrame([[email, senha_hash, nome]], columns=['email', 'senha', 'nome'])
        df = pd.concat([df, novo_usuario], ignore_index=True)
        df.to_csv(caminho_csv, index=False)
        return True, "Cadastro realizado com sucesso!"
        
    except FileNotFoundError:
        return False, "Erro: arquivo de dados não encontrado."
    except Exception as e:
        return False, f"Erro ao salvar: {str(e)}"