import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from enum import Enum


class TipoGrafico(Enum):
    TODASUNI = 0
    UMAUNI = 1


#-------------------------------------Constantes---------------------------------------------

ANO_INICIAL = '2010'
ANO_FINAL = '2014'

csvList = {'2010': 'bolsas_vs_desist-2010-RS', '2011': 'bolsas_vs_desist-2011-RS', '2012': 'bolsas_vs_desist-2012-RS',
           '2013': 'bolsas_vs_desist-2013-RS',
           '2014': 'bolsas_vs_desist-2014-RS'}

columns = ['Nome da Instituição', 'Count',
           'Nome do Curso de Graduação', 'Quantia de Bolsas',
           'Código do Curso de Graduação', 'Quantidade de Ingressantes no Curso',
           'Quantidade de Desistências',
           'Nome da Área do Curso segundo a classificação CINE BRASIL',
           'Percentual de Bolsas', 'Taxa de Desistência Acumulada', 'Ano de Ingresso']

def read_csv(file_path, delimiter=";", encoding='cp1252'):
    file_path = "arquivosCSV/bolsas_vs_desist/"+file_path+".csv"
    return pd.read_csv(file_path, delimiter=delimiter, encoding=encoding)


def filter_data(df, graph_type):
    df = df[df['Nome do Curso de Graduação'] == course]

    if graph_type == TipoGrafico.UMAUNI:
        df = df[df['Nome da Instituição'] == university]

    return df


def calculate_percentages(df):
    df['Taxa de Desistência Acumulada'] = (
            df['Quantidade de Desistências'] / df['Quantidade de Ingressantes no Curso'] * 100).round(2).astype(
        float)
    return df


def plot_graph(df, graph_type):
    if graph_type == TipoGrafico.TODASUNI:
        df.plot(kind='scatter', x='Percentual de Bolsas', y='Taxa de Desistência Acumulada', color='CornflowerBlue')
        plt.xscale('log')
        x_ticks = [1, 10, 100]
        plt.xticks(x_ticks, labels=[str(x) for x in x_ticks])
    else:
        graph = sns.lmplot(x="Percentual de Bolsas", y="Taxa de Desistência Acumulada", hue="Ano de Ingresso", data=df, fit_reg=False)
        plt.xscale('log')
        x_ticks = [1, 10, 100]
        plt.xticks(x_ticks, labels=[str(x) for x in x_ticks])

    plt.title(course if graph_type == TipoGrafico.TODASUNI else university)
    plt.suptitle(course if graph_type != TipoGrafico.TODASUNI else "")
    plt.xlabel('Percentual Bolsas')
    plt.ylabel('Percentual Desistência')
    plt.grid(True)
    plt.show()

#------------------------Input--------------------------

def read_tipo_graf():
    print("0: Múltiplas universidades")
    print("1: Uma universidade")
    user_input = input("Tipo gráfico: ").strip()

    # Attempt to convert input to integer
    try:
        int_user_input = int(user_input)
    except ValueError:
        print("Entrada não é um número inteiro!")
        return

    # Attempt to convert integer to TipoGrafico enumeration
    try:
        input_graph_type = TipoGrafico(int_user_input)
    except ValueError:
        print("Essa não é uma escolha válida!")
    1
    return input_graph_type

def read_todas_uni():
    ano_selecionado = input("Ano [2010 - 2014 ou ALL]: ").strip()
    # Lê de todos os anos.
    if ano_selecionado == "ALL":
        df_list = [read_csv(csv) for csv in csvList.values()]
        dfLido = pd.concat(df_list, ignore_index=True)
    # Lê só de um ano selecionado.
    else:
        dfLido = read_csv(csvList.get(ano_selecionado))
    return dfLido

def read_uma_uni():
    anoNum = 2010
    df_list = []
    for csv in csvList.values():
        df = read_csv(csv)
        df['Ano de Ingresso'] = str(anoNum)
        df_list.append(df)
        anoNum += 1
    dfTodosAnos = pd.concat(df_list, ignore_index=True)
    return dfTodosAnos

#-----------------------Execução---------------------------
course = "ciência da computação"
university = "pontifícia universidade católica do rio grande do sul"

graphType = read_tipo_graf()

if graphType == TipoGrafico.TODASUNI:
    df = read_todas_uni()
else:
    df = read_uma_uni()
            
df = filter_data(df, graphType)
df = calculate_percentages(df)
plot_graph(df, graphType)
