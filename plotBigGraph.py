import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import filterData as fd

#-------------------------------------Constantes---------------------------------------------
csvList = {'2010': 'bolsasDesist2010RS', '2011': 'bolsasDesist2011RS', '2012': 'bolsasDesist2012RS', '2013': 'bolsasDesist2013RS', 
          '2014': 'bolsasDesist2014RS'}

columns = ['Nome da Instituição', 'Count',
       'Nome do Curso de Graduação', 'Quantia de Bolsas',
       'Código do Curso de Graduação', 'Quantidade de Ingressantes no Curso',
       'Quantidade de Desistências',
       'Nome da Grande Área do Curso segundo a classificação CINE BRASIL',
       'Percentual de Bolsas', 'Taxa de Desistência Acumulada', 'Ano de Ingresso']

# Nome da área ou curso selecionado.
selected = "ciência da computação"
# Boleano indica se selected é área [1] ou curso[0].
area = 0
# Nome da universidade selecionado, utilizado apenas para gráfico do tipo "uma universidade em diferentes anos".
university = "pontifícia universidade católica do rio grande do sul"

#-------------------------------------Gráfico-----------------------------------------

# Seleciona entre gráfico de múltiplas universidades em um ano (0) ou uma única universidade em múltiplos anos (1).
while(True):
    graphType = int(input(" Multiplas universidades[0] ou uma universidade [1]: "))
    if(graphType == 0 or graphType == 1):
        break
    else:
        print(" Digite 0 ou 1!")
        input(" Precione Enter para continuar...")

#--------Gráfico de Múltiplas Universidades em um Ano---------
if(graphType == 0):
    anoStr = input(" Escolha um ano [2010 - 2014]: ")
    filtered_df = fd.filterData(csvList[anoStr], selected,  area)

    # Plota gráfico
    sns.regplot(x="Percentual de Bolsas", y="Taxa de Desistência Acumulada", order = 2, data=filtered_df, ci=None, color='CornflowerBlue', line_kws={"color": "darkgray"})
    sns.regplot(x="Percentual de Bolsas", y="Taxa de Desistência Acumulada", order = 1, data=filtered_df, ci=None, color='CornflowerBlue', line_kws={"color": "dimgray"})

#--------Gráfico de uma Universidade em Múltiplos Anos--------
else:
    # Lê universidade. Comente caso fique chato digitar o nome da universidade no console.
    # print(" Escolha uma universidade: ")
    # university = input()

    # Lê e filtra csv de cada ano por área ou curso e universidade.
    # Adiciona a data filtrada para cada ano a uma lista que é transformada em um dataframe final que une todos os anos. 
    filtered_list = []
    anoNum = 2010
    for csv in csvList.values():
        data = fd.filterData(csv, selected, area, university).values.tolist()
        if(data):
            data[0].append(str(anoNum))
            filtered_list.append(data[0])
        anoNum += 1
    filtered_df = pd.DataFrame(filtered_list, columns=columns)

    # Plota gráfico.
    # Desenha pontos com legenda para cada ano no gráfico.
    graph = sns.lmplot(x="Percentual de Bolsas", y="Taxa de Desistência Acumulada", hue="Ano de Ingresso", data=filtered_df, fit_reg=False)
    # Desenha regressão linear.
    sns.regplot(x="Percentual de Bolsas", y="Taxa de Desistência Acumulada", order = 2, data=filtered_df, ci=None, scatter=False, ax=graph.axes[0, 0], line_kws={"color": "darkgray"})
    sns.regplot(x="Percentual de Bolsas", y="Taxa de Desistência Acumulada", order = 1, data=filtered_df, ci=None, scatter=False, ax=graph.axes[0, 0], line_kws={"color": "dimgray"})
    # Salva csv de teste.
    # filtered_df.to_csv('arquivosCSV/teste/testeUni.csv', encoding='cp1252', sep=';')
    # filtered_df.reset_index(drop=True, inplace=True)
    
#------------------------------------Legendas--------------------------------------------
#Add title and labels
if(graphType == 0):
    plt.title(selected)
else:
    plt.title(university)
    plt.suptitle(selected)
plt.xlabel('Percentual Bolsas')
plt.ylabel('Percentual Desistência')

#Show the plot
plt.grid(True)

plt.show()