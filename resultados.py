import os

from easygui import msgbox


def mostrar_resultados(diferencas: dict, diferenca_total: float):
    html = '<html><head><title>Resultados</title></head><body>'
    html += '<h1>Resultados Comparativo de Créditos e Liquidações</h1>'
    html += '<br>'
    html += '<h2>Diferença total: R$' + str(round(diferenca_total, 2)) + '</h2>'
    html += '<br>'
    html += '<table border="1">'
    html += '<tr>'
    html += '<th>Data</th>'
    html += '<th>Crédito</th>'
    html += '<th>Liquidação</th>'
    html += '<th>Diferença</th>'
    html += '</tr>'
    
    for data in diferencas:
        html += '<tr>'
        html += '<td>' + str(data) + '</td>'
        html += '<td>' + str(diferencas[data]['credito']) + '</td>'
        html += '<td>' + str(diferencas[data]['liquidacao']) + '</td>'
        html += '<td>' + str(diferencas[data]['diferenca']) + '</td>'
        html += '</tr>'
        
    html += '</table>'
    
    html += '</body></html>'
    
    nome_arquivo_resultados = 'comparativo_creditos_liquidacoes.html'
    with open(nome_arquivo_resultados, 'w') as file:
        file.write(html)
        
    os.system(nome_arquivo_resultados)
    
    msgbox('Resultados salvos em ' + os.getcwd() + '/' + nome_arquivo_resultados)