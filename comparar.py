from easygui import msgbox
import pandas as pd
from pcld_user_gui import get_arquivos_pcld_do_usuario
from resultados import mostrar_resultados, mostrar_resultados_pcld
from user_gui import get_arquivos_do_usuario


def comparar_creditos_com_liquidacoes(is_test=False):
    creditos, liquidacoes = get_arquivos_do_usuario(is_test)
    if creditos.empty or liquidacoes.empty:
        msgbox("Erro ao obter arquivos de créditos e liquidações.")
    
    total_diario_creditos = get_totais_diarios(creditos, 'Data', 'Valor')
    total_diario_liquidacoes = get_totais_diarios(liquidacoes, 'Liquidação', 'Valor Pago')
    
    diferencas = {}
    diferenca_total = 0
    
    for data in total_diario_creditos:
        if data in total_diario_liquidacoes:
            diferenca = total_diario_creditos[data] - total_diario_liquidacoes[data]
            
            if diferenca == 0:
                continue
            
            data_str = data.strftime('%d/%m/%Y')
            
            diferencas[data_str] = {
                'credito': round(total_diario_creditos[data], 2),
                'liquidacao': round(total_diario_liquidacoes[data], 2),
                'diferenca': round(diferenca, 2)
            }
            diferenca_total += diferenca
            
    mostrar_resultados(diferencas, diferenca_total)
            
    return diferencas, diferenca_total
        
def get_totais_diarios(dataframe, coluna_data, coluna_valor):
    totais_diarios = {}
    
    for index, row in dataframe.iterrows():
        data = row[coluna_data]
        valor = row[coluna_valor]
        
        is_valor_float = isinstance(valor, float)
        is_valor_int = isinstance(valor, int)
        is_valor_str = isinstance(valor, str)
        
        if not is_valor_float and not is_valor_int and not is_valor_str:
            continue
        
        if is_valor_str:
            valor = valor.replace('.', '')
            valor = valor.replace(',', '.')
            valor = valor.replace('C', '')
            valor = float(valor)
        
        if pd.isnull(data) or pd.isna(data):
            continue         
        
        if data not in totais_diarios:
            totais_diarios[data] = 0
            
        totais_diarios[data] += valor
        
    return totais_diarios

def comparar_pcld_com_posicoes_por_dia(is_test=False):
    pcld, posicoes_por_dia = get_arquivos_pcld_do_usuario(is_test)
    if pcld.empty or posicoes_por_dia.empty:
        msgbox("Erro ao obter arquivos de PCLD e Posições por Dia.")
    
    totais_pcld = get_totais_diarios(pcld, 'Liquidação', 'Valor do Titulo')
    totais_posicoes_por_dia = get_totais_diarios(posicoes_por_dia, 'Liquidação', 'Valor Pago')
    
    diferencas = {}
    
    for data in totais_pcld:
        if data in totais_posicoes_por_dia:
            diferenca = totais_pcld[data] - totais_posicoes_por_dia[data]
            if diferenca == 0:
                continue
            
            data_str = data.strftime('%d/%m/%Y')
            
            diferencas[data_str] = {
                'pcld': round(totais_pcld[data], 2),
                'posicoes_por_dia': round(totais_posicoes_por_dia[data], 2),
                'diferenca': round(diferenca, 2)
            }
            
            
    mostrar_resultados_pcld(diferencas)
    
    return diferencas


if __name__ == '__main__':
    print("Escolha uma opção:")
    print("1 - Comparar créditos com liquidações")
    print("2 - Comparar PCLD com Posições por Dia")
    opcao = input()
    print('Opção escolhida:', opcao)
    
    if opcao == '1':    
        diferencas, diferenca_total = comparar_creditos_com_liquidacoes(True)
    elif opcao == '2':
        comparar_pcld_com_posicoes_por_dia(True)
    else:
        print("Opção inválida.")
        exit()