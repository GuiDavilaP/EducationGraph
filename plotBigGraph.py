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


import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

def plot_graph(df, graph_type, selected, university="none"):
    # Ensure data is suitable for logarithmic scale
    df = df[df['Percentual de Bolsas'] > 0]  # Filter out non-positive values

    # Plot the graph using pandas
    if graph_type == 0:
        df.plot(kind='scatter', x='Percentual de Bolsas', y='Taxa de Desistência Acumulada', color='CornflowerBlue')
        plt.xscale('log')  # Set x-axis to logarithmic scale

        # Set x-axis ticks
        x_ticks = [1, 10, 100]  # Example ticks for a logarithmic scale
        plt.xticks(x_ticks, labels=[str(x) for x in x_ticks])  # Set ticks and labels
    else:
        graph = sns.lmplot(x="Percentual de Bolsas", y="Taxa de Desistência Acumulada", hue="Ano de Ingresso", data=df,
                           fit_reg=False)
        graph.set(xscale="log")
        sns.regplot(x="Percentual de Bolsas", y="Taxa de Desistência Acumulada", order=2, data=df, ci=None,
                    scatter=False, ax=graph.axes[0, 0], line_kws={"color": "darkgray"}, x_bins=20)  # Adjust x_bins as needed
        sns.regplot(x="Percentual de Bolsas", y="Taxa de Desistência Acumulada", order=1, data=df, ci=None,
                    scatter=False, ax=graph.axes[0, 0], line_kws={"color": "dimgray"}, x_bins=20)  # Adjust x_bins as needed

    # Set plot limits if necessary
    # Example: plt.xlim(left=1) to ensure the x-axis starts from 1

    # Configure and display the plot as before
    plt.title(selected if graph_type == 0 else university)
    plt.suptitle(selected if graph_type != 0 else "")
    plt.xlabel('Percentual Bolsas')
    plt.ylabel('Percentual Desistência')
    plt.grid(True)
    plt.show()

    # Exibir o gráfico
    plt.show()

# Exemplo de uso das funções
file_path = 'arquivosCSV/bolsas_vs_desist/bolsas_vs_desist-2010-RS.csv'
df = read_csv(file_path)
df_filtered = filter_data(df, "ciência da computação", "curso")
df_percentages = calculate_percentages(df_filtered)
plot_graph(df_percentages, 0, "ciência da computação")
