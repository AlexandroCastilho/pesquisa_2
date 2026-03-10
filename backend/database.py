import pandas as pd
import os
from datetime import datetime

CAMINHO_RESPOSTAS = os.path.join('backend', 'data', 'respostas.csv')

def salvar_pesquisa(dados):
    try:
        # Adiciona a data/hora da resposta
        dados['data_hora'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        df_nova_resposta = pd.DataFrame([dados])

        if not os.path.exists(CAMINHO_RESPOSTAS):
            df_nova_resposta.to_csv(CAMINHO_RESPOSTAS, index=False)
        else:
            df_nova_resposta.to_csv(CAMINHO_RESPOSTAS, mode='a', header=False, index=False)
        
        return True
    except Exception as e:
        print(f"Erro ao salvar pesquisa: {e}")
        return False

def carregar_respostas():
    try:
        if os.path.exists(CAMINHO_RESPOSTAS):
            return pd.read_csv(CAMINHO_RESPOSTAS)
        return pd.DataFrame() # Retorna vazio se não houver dados
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

CAMINHO_CONFIG = os.path.join('backend', 'data', 'config_pesquisa.csv')
CAMINHO_CLIENTES = os.path.join('backend', 'data', 'base_clientes.csv')

def salvar_config_perguntas(lista_perguntas):
    df = pd.DataFrame(lista_perguntas, columns=['pergunta'])
    df.to_csv(CAMINHO_CONFIG, index=False)

def carregar_config_perguntas():
    if os.path.exists(CAMINHO_CONFIG):
        return pd.read_csv(CAMINHO_CONFIG)['pergunta'].tolist()
    return ["Qual sua nota geral?"] # Pergunta padrão caso esteja vazio