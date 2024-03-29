import datetime
from easygui import msgbox
import pandas as pd
from pcld_user_gui import get_arquivos_pcld_do_usuario
from resultados import mostrar_resultados, mostrar_resultados_pcld
from user_gui import get_arquivos_do_usuario        
        
def normalize_valor(valor):
    if isinstance(valor, float):
        return valor
    
    if isinstance(valor, int):
        return float(valor)
    
    if not isinstance(valor, str):
        return None
    
    valor = valor.replace('.', '')
    valor = valor.replace(',', '.')
    valor = valor.replace('C', '')
    
    return float(valor)

def normalize_nota_fiscal(nota_fiscal):
    if not isinstance(nota_fiscal, str):
        nota_fiscal = str(nota_fiscal)
    
    if nota_fiscal == 'nan' or pd.isnull(nota_fiscal) or pd.isna(nota_fiscal) or nota_fiscal == '0' or nota_fiscal == '':
        return None
        
    nota_fiscal = nota_fiscal.replace('.', '')
    nota_fiscal = nota_fiscal.split('/')[0]
    
    return nota_fiscal

def get_diferencas_entre_dataframes(totals_1, totals_2, coluna_totals_1, coluna_totals_2, datas_1, datas_2):
    diferencas = {}
    dados_sem_diferenca = 0
    for dado in totals_1:
        dado1 = totals_1[dado]
        dado2 = totals_2[dado] if dado in totals_2 else 0
            
        diferenca = dado1 - dado2
        if diferenca == 0:
            dados_sem_diferenca += 1
            continue
        
        diferencas[dado] = {
            coluna_totals_1: round(dado1, 2),
            coluna_totals_2: round(dado2, 2),
            'diferenca': round(diferenca, 2),
            'datas ' + coluna_totals_1: ', '.join(datas_1[dado]) if dado in datas_1 else 'Sem datas',
            'datas ' + coluna_totals_2: ', '.join(datas_2[dado]) if dado in datas_2 else 'Sem datas'
        }
    
    for dado in totals_2:
        if dado not in totals_1:
            diferencas[dado] = {
                coluna_totals_1: 0,
                coluna_totals_2: round(totals_2[dado], 2),
                'diferenca': round(totals_2[dado], 2),
                'datas ' + coluna_totals_1: 'Sem datas',
                'datas ' + coluna_totals_2: ', '.join(datas_2[dado]) if dado in datas_2 else 'Sem datas'
            }
            
    return diferencas, dados_sem_diferenca

def get_totais_diarios(dataframe, coluna_data, coluna_valor):
    totais_diarios = {}
    
    for index, row in dataframe.iterrows():
        data = row[coluna_data]
        valor = row[coluna_valor]
        
        valor = normalize_valor(valor)
        if valor is None:
            continue
        
        if pd.isnull(data) or pd.isna(data):
            continue         
        
        if data not in totais_diarios:
            totais_diarios[data] = 0
            
        totais_diarios[data] += valor
        
    return totais_diarios

def get_valores_notas_fiscais(dataframe, coluna_nota_fiscal, coluna_valor, coluna_data):
    valores_notas_fiscais = {}
    datas_notas_fiscais = {}
    
    for index, row in dataframe.iterrows():
        nota_fiscal = row[coluna_nota_fiscal]
        valor = row[coluna_valor]
        data = row[coluna_data]
        
        valor = normalize_valor(valor)
        if valor is None:
            continue
        
        nota_fiscal_normalizada = normalize_nota_fiscal(nota_fiscal)
        if nota_fiscal_normalizada is None:
            continue
        
        if nota_fiscal_normalizada not in valores_notas_fiscais:
            valores_notas_fiscais[nota_fiscal_normalizada] = 0
        
        if nota_fiscal_normalizada not in datas_notas_fiscais:
            datas_notas_fiscais[nota_fiscal_normalizada] = []
        
        data_dd_mm_yyyy = data.strftime('%d/%m/%Y') if isinstance(data, pd.Timestamp) else str(data)
        if ' 00:00:00' in data_dd_mm_yyyy:
            data_dd_mm_yyyy = data_dd_mm_yyyy.split(' ')[0]
            data_dd_mm_yyyy = datetime.datetime.strptime(data_dd_mm_yyyy, '%Y-%m-%d').strftime('%d/%m/%Y')
        if '-' in data_dd_mm_yyyy:
            data_dd_mm_yyyy = data_dd_mm_yyyy.split('-')[1] + '/' + data_dd_mm_yyyy.split('-')[0] + '/' + data_dd_mm_yyyy.split('-')[2]  
        
        valores_notas_fiscais[nota_fiscal_normalizada] += valor
        datas_notas_fiscais[nota_fiscal_normalizada].append(str(data_dd_mm_yyyy))
        
    return valores_notas_fiscais, datas_notas_fiscais

def comparar_pcld_com_posicoes_por_dia(is_test=False):
    pcld, posicoes_por_dia = get_arquivos_pcld_do_usuario(is_test)
    if pcld.empty or posicoes_por_dia.empty:
        msgbox("Erro ao obter arquivos de PCLD e Posições por Dia.")
    
    totais_notas_pcld, datas_notas_pcld = get_valores_notas_fiscais(pcld, 'N. Doc', 'Valor do Titulo', 'Liquidação')
    totais_notas_posicoes_por_dia, data_notas_posicoes_por_dia = get_valores_notas_fiscais(posicoes_por_dia, 'Num. Titulo', 'Valor Pago', 'Liquidação')
    
    diferencas, notas_sem_diferenca = get_diferencas_entre_dataframes(totais_notas_pcld, totais_notas_posicoes_por_dia, 'pcld', 'posicoes_por_dia', datas_notas_pcld, data_notas_posicoes_por_dia)
            
            
    mostrar_resultados_pcld(diferencas)
    msgbox('Notas sem diferença (OK): ' + str(notas_sem_diferenca))
    
    return diferencas

def comparar_creditos_com_liquidacoes(is_test=False):
    creditos, liquidacoes = get_arquivos_do_usuario(is_test)
    if creditos.empty or liquidacoes.empty:
        msgbox("Erro ao obter arquivos de créditos e liquidações.")    
    
    total_notas_creditos, datas_notas_creditos = get_valores_notas_fiscais(creditos, 'Nº Doc.', 'Valor', 'Data')
    total_notas_liquidacoes, datas_notas_liquidacoes = get_valores_notas_fiscais(liquidacoes, 'Num. Titulo', 'Valor Pago', 'Liquidação')
    
    diferencas, notas_sem_diferenca = get_diferencas_entre_dataframes(total_notas_creditos, total_notas_liquidacoes, 'credito', 'liquidacao', datas_notas_creditos, datas_notas_liquidacoes)
            
    mostrar_resultados(diferencas)
    msgbox('Notas sem diferença (OK): ' + str(notas_sem_diferenca))
            
    return diferencas

if __name__ == '__main__':
    print("Escolha uma opção:")
    print("1 - Comparar créditos com liquidações")
    print("2 - Comparar PCLD com Posições por Dia")
    opcao = input()
    print('Opção escolhida:', opcao)
    
    if opcao == '1':    
        comparar_creditos_com_liquidacoes(True)
    elif opcao == '2':
        comparar_pcld_com_posicoes_por_dia(True)
    else:
        print("Opção inválida.")
        exit()