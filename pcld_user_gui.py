
import os
import pandas as pd
from easygui import msgbox, diropenbox
from config import get_config

def get_arquivos_pcld_do_usuario(is_test=False):
    
    #with easygui the user select folder with files.
    mensagem = "Selecione a pasta com os arquivos PCLD. \n O arquivo de Base deve possuir 'PCLD' no nome e o de posicoes do dia 'PosicaoPorDia'."
    
    if not is_test:
        msgbox(mensagem)
    
    if not is_test:
        path = diropenbox(mensagem)
    else:
        path = get_config(['test', 'pcld_path'])
    
    if not path:
        msgbox("Nenhuma pasta foi selecionada.")
        return None, None
    
    arquivos_dentro_da_pasta = os.listdir(path)
    
    arquivo_pcld = None
    arquivos_posicoes_dia = []    
    
    for arquivo in arquivos_dentro_da_pasta:
        if 'PCLD'.lower() in arquivo.lower() and '.xls' in arquivo.lower():
            arquivo_pcld = path + '/' + arquivo
        elif 'PosicaoPorDia'.lower() in arquivo.lower() and '.xls' in arquivo.lower():
            arquivos_posicoes_dia.append(path + '/' + arquivo)
            
    if not arquivo_pcld:
        msgbox("Não foi encontrado o arquivo de PCLD.")
        return None, None
    elif not arquivos_posicoes_dia:
        msgbox("Não foi encontrado o arquivo de Posicoes do Dia.")
        return None, None
        
    pcld = get_pcld(arquivo_pcld)
    posicoes_por_dia = get_posicoes_por_dia(arquivos_posicoes_dia)    
    
    return pcld, posicoes_por_dia

def get_pcld(arquivo_pcld): 
    cols = ['Unidade', 'Cobrança', 'N. Doc', 'Emissão', 'Vencimento', 'Liquidação', 'Cliente', 'Banco', 'Valor do Titulo']

    dataframe = pd.DataFrame()
    
    try:
        excel_data = pd.read_excel(arquivo_pcld, sheet_name=None)
    except FileNotFoundError:
        print("Arquivo não encontrado:", arquivo_pcld)
        return dataframe
    
    for sheet_name, sheet_data in excel_data.items():
        if all(col in sheet_data.columns for col in cols):
            dataframe = pd.concat([dataframe, sheet_data[cols]])

    return dataframe

def get_posicoes_por_dia(arquivos_posicoes_dia):
    cols = ['Base', 'Num. Titulo', 'Emissão', 'Codigo Cliente', 'Nome Cliente', 'Cobrança', 'Conta', 'Valor Titulo', 'Valor em Aberto', 'Valor Pago', 'Vencimento', 'Liquidação']
    
    dataframe = pd.DataFrame()
    
    for arquivo in arquivos_posicoes_dia:
        dataframe = pd.concat([dataframe, pd.read_excel(arquivo, usecols=cols)])
    
    return dataframe

if __name__ == "__main__":
    pcld, posicoes_por_dia = get_arquivos_pcld_do_usuario(is_test=True)
    
    print(pcld)
    print(posicoes_por_dia)