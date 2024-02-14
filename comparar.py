import pandas as pd
from user_gui import get_arquivos_do_usuario


def comparar_creditos_com_liquidacoes(is_test=False):
    creditos, liquidacoes = get_arquivos_do_usuario(is_test)
    
    total_diario_creditos = get_totais_diarios(creditos, 'Data', 'Valor')
    total_diario_liquidacoes = get_totais_diarios(liquidacoes, 'Liquidação', 'Valor Pago')
    
    diferencas = {}
    diferenca_total = 0
    
    for data in total_diario_creditos:
        if data in total_diario_liquidacoes:
            diferenca = total_diario_creditos[data] - total_diario_liquidacoes[data]
            diferencas[data] = {
                'credito': round(total_diario_creditos[data], 2),
                'liquidacao': round(total_diario_liquidacoes[data], 2),
                'diferenca': round(diferenca, 2)
            }
            diferenca_total += diferenca
            
            
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


if __name__ == '__main__':
    diferencas, diferenca_total = comparar_creditos_com_liquidacoes(True)
    
    print(diferencas)
    print(diferenca_total)