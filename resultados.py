import os
import subprocess

from easygui import msgbox
import pandas as pd


def mostrar_resultados(diferencas: dict, diferenca_total: float):
    df = pd.DataFrame.from_dict(diferencas, orient='index', columns=['credito', 'liquidacao', 'diferenca'])
    df.index.name = 'Data'

    nome_arquivo_resultados = 'comparativo_creditos_liquidacoes.xlsx'
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    file_path = os.path.join(desktop_path, nome_arquivo_resultados)
    df.to_excel(file_path)
    
    subprocess.Popen(['start', file_path], shell=True)

    msgbox('Resultados salvos em ' + file_path)



def mostrar_resultados_pcld(diferencas: dict):
    df = pd.DataFrame.from_dict(diferencas, orient='index', columns=['pcld', 'posicoes_por_dia', 'diferenca'])
    df.index.name = 'Data'

    nome_arquivo_resultados = 'comparativo_pcld_posicoes_por_dia.xlsx'
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    file_path = os.path.join(desktop_path, nome_arquivo_resultados)
    df.to_excel(file_path)
    
    subprocess.Popen(['start', file_path], shell=True)

    msgbox('Resultados salvos em ' + file_path)