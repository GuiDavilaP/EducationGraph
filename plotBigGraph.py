import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

#from filterData import filterData
ANO_INICIAL = '2010'
ANO_FINAL = '2014'

#-------------------------------------Constantes---------------------------------------------
csvList = {'2010': 'bolsas_vs_desist-2010-RS', '2011': 'bolsas_vs_desist-2011-RS', '2012': 'bolsas_vs_desist-2012-RS',
           '2013': 'bolsas_vs_desist-2013-RS',
           '2014': 'bolsas_vs_desist-2014-RS'}

columns = ['Nome da Instituição', 'Count',
           'Nome do Curso de Graduação', 'Quantia de Bolsas',
           'Código do Curso de Graduação', 'Quantidade de Ingressantes no Curso',
           'Quantidade de Desistências',
           'Nome da Grande Área do Curso segundo a classificação CINE BRASIL',
           'Percentual de Bolsas', 'Taxa de Desistência Acumulada', 'Ano de Ingresso']

# Nome da área ou curso selecionado.
selected = "ciência da computação"

# Nome da universidade selecionado, utilizado apenas para gráfico do tipo "uma universidade em diferentes anos".
university = "pontifícia universidade do rio grande do sul"


def read_csv(file_path, delimiter=";", encoding='cp1252'):
    return pd.read_csv(file_path, delimiter=delimiter, encoding=encoding)


def filter_data(df, selected, filter_type="curso", university="none"):
    if filter_type == "area":
        df = df[df['Nome da Grande Área do Curso segundo a classificação CINE BRASIL'] == selected]

    elif filter_type == "curso":
        df = df[df['Nome do Curso de Graduação'] == selected]

    if university != "none":
        df = df[df['Nome da Instituição'] == university]
    return df

def calculate_percentages(df):
    df['Percentual de Bolsas'] = (df['Quantia de Bolsas'] / df['Quantidade de Ingressantes no Curso'] * 100).round(
        2).astype(float)
    df['Taxa de Desistência Acumulada'] = (
            df['Quantidade de Desistências'] / df['Quantidade de Ingressantes no Curso'] * 100).round(2).astype(
        float)
    return df


def plot_graph(df, graph_type, selected, university="none"):
    # Plotar o gráfico
    if graph_type == 0:
        sns.regplot(x="Percentual de Bolsas", y="Taxa de Desistência Acumulada", order=1, data=df, ci=None,
                    color='CornflowerBlue', line_kws={"color": "dimgray"})
    else:
        graph = sns.lmplot(x="Percentual de Bolsas", y="Taxa de Desistência Acumulada", hue="Ano de Ingresso", data=df,
                           fit_reg=False)
        sns.regplot(x="Percentual de Bolsas", y="Taxa de Desistência Acumulada", order=2, data=df, ci=None,
                    scatter=False, ax=graph.axes[0, 0], line_kws={"color": "darkgray"})
        sns.regplot(x="Percentual de Bolsas", y="Taxa de Desistência Acumulada", order=1, data=df, ci=None,
                    scatter=False, ax=graph.axes[0, 0], line_kws={"color": "dimgray"})

    # Configurar o gráfico
    if graph_type == 0:
        plt.title(selected)
    else:
        plt.title(university)
        plt.suptitle(selected)
    plt.xlabel('Percentual Bolsas')
    plt.ylabel('Percentual Desistência')
    plt.grid(True)

    # Exibir o gráfico
    plt.show()


# Exemplo de uso das funções
file_path = 'arquivosCSV/bolsas_vs_desist/bolsas_vs_desist-2010-RS.csv'
df = read_csv(file_path)
df_filtered = filter_data(df, "ciência da computação", "curso")
df_percentages = calculate_percentages(df_filtered)
plot_graph(df_percentages, 0, "ciência da computação")
