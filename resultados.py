import os
import pandas as pd
from easygui import msgbox

def renderizar_resultados(diferencas: dict, nome_arquivo_resultados: str, coluna_totals_1: str, coluna_totals_2: str, coluna_diferenca: str, coluna_index: str):
    diferencas_ordenadas_pelo_index = dict(sorted(diferencas.items(), key=lambda item: item[0]))
    
    df = pd.DataFrame.from_dict(diferencas_ordenadas_pelo_index, orient='index', columns=[coluna_totals_1, coluna_totals_2, coluna_diferenca, 'datas ' + coluna_totals_1, 'datas ' + coluna_totals_2])
    df.index.name = coluna_index

    try:
        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        file_path = os.path.join(desktop_path, nome_arquivo_resultados)
        df.to_excel(file_path)
    except Exception as e:
        msgbox('Erro ao salvar resultados. Por favor, feche o arquivo se ele estiver aberto e tente novamente.')
        return

    msgbox('Resultados salvos na área de trabalho: ' + file_path)


def mostrar_resultados(diferencas: dict):
    renderizar_resultados(diferencas, 'comparativo_creditos_liquidacoes.xlsx', 'credito', 'liquidacao', 'diferenca', 'Nota Fiscal')

def mostrar_resultados_pcld(diferencas: dict):    
    renderizar_resultados(diferencas, 'comparativo_pcld_posicoes_por_dia.xlsx', 'pcld', 'posicoes_por_dia', 'diferenca', 'Nota Fiscal')
    