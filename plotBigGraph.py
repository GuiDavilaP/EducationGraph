import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from enum import Enum


class TipoGrafico(Enum):
    TODASUNI = 0,
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

# Nome da área ou curso selecionado.
selected = "ciência da computação"

# Nome da universidade selecionado, utilizado apenas para gráfico do tipo "uma universidade em diferentes anos".
university = "pontifícia universidade católica do rio grande do sul"


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
    df['Taxa de Desistência Acumulada'] = (
            df['Quantidade de Desistências'] / df['Quantidade de Ingressantes no Curso'] * 100).round(2).astype(
        float)
    return df


def plot_graph(df, graph_type, selected, university_name="none"):
    # Plot the graph using pandas
    if graph_type == TipoGrafico.TODASUNI:
        df.plot(kind='scatter', x='Percentual de Bolsas', y='Taxa de Desistência Acumulada', color='CornflowerBlue')
        plt.xscale('log')  # Set x-axis to logarithmic scale
        # Set x-axis ticks
        x_ticks = [1, 10, 100]
        plt.xticks(x_ticks, labels=[str(x) for x in x_ticks])  # Set ticks and labels
    else:
        filtered_list = []
        anoNum = 2010

        for i in range(5):
            filtered_list.append(df[df['Ano de Ingresso'] == str(anoNum + i)])

        for i in range(5):
            plt.scatter(filtered_list[i]['Percentual de Bolsas'], filtered_list[i]['Taxa de Desistência Acumulada'], label=str(anoNum + i))
            plt.xscale('log')

        plt.legend()
        plt.xticks([1, 10, 100], labels=[str(x) for x in [1, 10, 100]])


    # Configure and display the plot as before
    plt.title(selected if graph_type == TipoGrafico.TODASUNI else university_name)
    plt.suptitle(selected if graph_type != TipoGrafico.TODASUNI else "")
    plt.xlabel('Percentual Bolsas')
    plt.ylabel('Percentual Desistência')
    plt.grid(True)
    plt.show()

    # Exibir o gráfico
    plt.show()


# Exemplo de uso das funções
file_path = 'arquivosCSV/bolsas_vs_desist/bolsas_vs_desist-2010-RS.csv'
df = read_csv(file_path)

df_filtered = filter_data(df, "ciência da computação", "curso", "pontifícia universidade católica do rio grande do sul")
df_percentages = calculate_percentages(df_filtered)
plot_graph(df_percentages, TipoGrafico.UMAUNI, "ciência da computação")
