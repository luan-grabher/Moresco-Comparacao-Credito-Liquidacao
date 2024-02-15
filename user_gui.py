
import os
import pandas as pd
from easygui import msgbox, diropenbox
from config import get_config

def get_arquivos_do_usuario(is_test=False):
    
    #with easygui the user select folder with files.
    mensagem = "Selecione a pasta com os arquivos. \n O arquivo de credito deve possuir 'credito' no nome e o de liquidação 'liquidacao'."
    
    if not is_test:
        msgbox(mensagem)
    
    if not is_test:
        path = diropenbox(mensagem)
    else:
        path = get_config(['test', 'path'])
    
    if not path:
        msgbox("Nenhuma pasta foi selecionada.")
        return None, None
    
    arquivos_dentro_da_pasta = os.listdir(path)
    
    arquivo_creditos = None
    arquivos_liquidacoes = []    
    
    for arquivo in arquivos_dentro_da_pasta:
        if 'credito' in arquivo.lower() and '.xls' in arquivo.lower():
            arquivo_creditos = path + '/' + arquivo
        elif 'liquidacao' in arquivo.lower() and '.xls' in arquivo.lower():
            arquivos_liquidacoes.append(path + '/' + arquivo)
            
    if not arquivo_creditos:
        msgbox("Não foi encontrado o arquivo de créditos.")
        return None, None
    elif not arquivos_liquidacoes:
        msgbox("Não foi encontrado o arquivo de liquidações.")
        return None, None
    
    creditos = get_creditos(arquivo_creditos)
    liquidacoes = get_liquidacoes(arquivos_liquidacoes)
    
    return creditos, liquidacoes

def get_creditos(arquivo_creditos):
    try:
        #Data	Seqüência	Histórico	Contrapartida	Valor	Participante	Saldo	Filial	Usuário
        cols = ['Data', 'Histórico', 'Valor', 'Usuário']
        
        dataframe = pd.read_excel(arquivo_creditos, usecols=cols)

        return dataframe
    except Exception as e:
        msgbox("Erro ao ler arquivo de créditos. Por favor, feche o arquivo se ele estiver aberto e tente novamente.")
        return pd.DataFrame()

def get_liquidacoes(arquivos_liquidacoes):
    try:
        #Base	Num. Titulo	Emissão	Codigo Cliente	Nome Cliente	Banco	Cobrança	 Valor Titulo 	 Valor em Aberto 	 Valor Pago 	Vencimento	Liquidação
        cols = ['Base', 'Num. Titulo', 'Emissão', 'Codigo Cliente', 'Nome Cliente', 'Banco', 'Cobrança', 'Valor Titulo', 'Valor em Aberto', 'Valor Pago', 'Vencimento', 'Liquidação']
        
        dataframe = pd.DataFrame()
        
        for arquivo in arquivos_liquidacoes:
            dataframe = pd.concat([dataframe, pd.read_excel(arquivo, usecols=cols)])
        
        return dataframe
    except Exception as e:
        msgbox("Erro ao ler arquivo de liquidações. Por favor, feche o arquivo se ele estiver aberto e tente novamente.")
        return pd.DataFrame()

if __name__ == "__main__":
    creditos, liquidacoes = get_arquivos_do_usuario(is_test=True)
    
    print(creditos)
    print(liquidacoes)