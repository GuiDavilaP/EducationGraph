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
    df['Percentual de Bolsas'] = (df['Quantia de Bolsas'] / df['Quantidade de Ingressantes no Curso'] * 100).round(
        2).astype(float)
    df['Taxa de Desistência Acumulada'] = (
            df['Quantidade de Desistências'] / df['Quantidade de Ingressantes no Curso'] * 100).round(2).astype(
        float)
    return df


def plot_graph(df, graph_type, selected, university_name="none"):
    # Ensure data is suitable for logarithmic scale
    df = df[df['Percentual de Bolsas'] > 0]  # Filter out non-positive values

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
        for csv in csvList.values():
            # Leitura do arquivo CSV
            df = pd.read_csv('arquivosCSV/bolsas_vs_desist/' + csv + '.csv', delimiter=";", encoding='cp1252')

            # Filtragem dos dados
            df_filtered = filter_data(df, selected, university)

            # Verifica se o DataFrame não está vazio após a filtragem
            if not df_filtered.empty:
                # Cálculo dos percentuais
                df_calculated = calculate_percentages(df_filtered)

                # Verifica se o DataFrame calculado não está vazio
                if not df_calculated.empty:
                    # Converte DataFrame para lista de listas
                    data_list = df_calculated.values.tolist()
                    # Adiciona o ano à primeira lista de dados
                    data_list[0].append(str(anoNum))
                    # Adiciona a lista de dados filtrados à lista principal
                    filtered_list.append(data_list[0])

                # Incrementa o ano
                anoNum += 1
                # Imprime o nome do arquivo CSV processado
                print(csv)

        filtered_df = pd.DataFrame(filtered_list, columns=columns)
        # Plota gráfico.
        # Desenha pontos com legenda para cada ano no gráfico.
        sns.lmplot(x="Percentual de Bolsas", y="Taxa de Desistência Acumulada", hue="Ano de Ingresso", data=filtered_df,
                   fit_reg=False)

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
