import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import numpy as np
from matplotlib.colors import BoundaryNorm, ListedColormap
import matplotlib.patheffects as path_effects

#------------------------Configurações Gerais dos Mapas------------------------
def configure_plot():
    plt.rcParams.update({
        'font.size': 11,  # Tamanho da fonte geral
        'legend.fontsize': 7,  # Tamanho da fonte da legenda do gráfico de pizza
        'axes.titlesize': 15,  # Tamanho da fonte do título dos eixos
        'axes.labelsize': 13,  # Tamanho da fonte dos rótulos dos eixos
        'xtick.labelsize': 10,  # Tamanho da fonte dos valores da barra de cores (eixo x)
        'ytick.labelsize': 10   # Tamanho da fonte dos valores da barra de cores (eixo y)
    })

def plot_map(ax, mapa, column, cmap, legend_label, boundaries):
    norm = BoundaryNorm(boundaries, ncolors=len(boundaries)-1, clip=True)
    mapa.boundary.plot(ax=ax, linewidth=0.5)  # Plota as bordas do mapa
    mapa.plot(
        column=column,
        ax=ax,
        legend=True,
        cmap=cmap,
        norm=norm,
        legend_kwds={
            'label': legend_label,  # Rótulo da legenda
            'orientation': "horizontal",  # Orientação da barra de cores
            'boundaries': boundaries,  # Limites da barra de cores
            'ticks': boundaries,  # Valores dos ticks na barra de cores
            'shrink': 0.5  # Ajusta o tamanho da barra de cores
        }
    )

def show_map(title):
    plt.title(title)  # Define o título do mapa
    plt.axis('equal')  # Define a proporção igual para os eixos
    plt.show()  # Mostra o mapa

#-------------------------Mapa de Percentual de Bolsas -------------------------

def calculate_bolsas(dfzao):
    df_bolsas = dfzao.groupby('cod_estado').agg({
        'qtd_ingressantes': 'sum',
        'qtd_bolsas_parciais': 'sum',
        'qtd_bolsas_integrais': 'sum',
        'qtd_total_bolsas': 'sum',
    }).reset_index()

    df_bolsas['percentual_bolsas_parciais'] = (df_bolsas['qtd_bolsas_parciais'] / df_bolsas['qtd_total_bolsas']).round(2)
    df_bolsas['percentual_bolsas_integrais'] = (df_bolsas['qtd_bolsas_integrais'] / df_bolsas['qtd_total_bolsas']).round(2)
    df_bolsas['percentual_total_bolsas'] = (df_bolsas['qtd_total_bolsas'] / df_bolsas['qtd_ingressantes']).round(2)

    return df_bolsas

def add_pizza_graph(ax, mapa):
    for idx, row in mapa.iterrows():
        x, y = row.geometry.centroid.x, row.geometry.centroid.y
        sizes = [row['percentual_bolsas_parciais'], row['percentual_bolsas_integrais']]
        sizes = [0 if pd.isna(size) else size for size in sizes]

        if sum(sizes) == 0:
            continue

        if row['qtd_total_bolsas'] == 0 or pd.isna(row['qtd_total_bolsas']):
            size = 0.1
        else:
            size = min(1, (row['qtd_total_bolsas']) * 0.01)

        ax.pie(sizes, radius=size, center=(x, y), colors=['lightblue', 'blue'], startangle=90, counterclock=False, wedgeprops={'edgecolor': 'gray'})
        
        # Adiciona o percentual de bolsas integrais ao lado do gráfico de pizza
        text = ax.text(x + size, y, f"{row['percentual_bolsas_integrais']*100:.0f}%", fontsize=8, ha='left', va='center')
        text.set_path_effects([path_effects.Stroke(linewidth=1, foreground='white'), path_effects.Normal()])

    # Adiciona a legenda para os gráficos de pizza
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='lightblue', edgecolor='gray', label='Bolsas Parciais'),
        Patch(facecolor='blue', edgecolor='gray', label='Bolsas Integrais')
    ]
    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0.2, 0.8), title='Legenda')  # Move a legenda para a direita

def plot_mapa_bolsas(dfzao, mapa, sigla_curso):
    df_bolsas = calculate_bolsas(dfzao)
    mapa = mapa.merge(df_bolsas, how='left', left_on='CD_UF', right_on='cod_estado')

    configure_plot()
    _, ax = plt.subplots(1, figsize=(20, 15))  # Tamanho da janela
    boundaries = np.linspace(0, 0.6, 11)  # Limites da barra de cores
    cmap = ListedColormap([
        '#ffffcc', '#ffeda0', '#fed976', '#feb24c', '#fd8d3c', 
        '#fc4e2a', '#e31a1c', '#bd0026', '#800026', '#4d0019'
    ])  # Cores da barra de cores
    plot_map(ax, mapa, 'percentual_total_bolsas', cmap, "\nPercentual Bolsistas / Ingressantes", boundaries)
    add_pizza_graph(ax, mapa)
    title = f'Bolsistas Parciais e Integrais do ProUni em {sigla_curso} no Brasil (2010 - 2018)'
    show_map(title)

#---------------------------Mapa de Desistências-----------------------------

def plot_mapa_desist(dfzao, mapa, sigla_curso):
    # Desistências
    df_desistencias = dfzao.groupby('cod_estado').agg({
        'qtd_ingressantes': 'sum',
        'qtd_desistencias': 'sum',
    }).reset_index()

    # Recalcula taxa de desistência
    df_desistencias['taxa_desistencia'] = (
                df_desistencias['qtd_desistencias'] / df_desistencias['qtd_ingressantes']).round(2)

    # Mesclar com o GeoDataFrame
    mapa = mapa.merge(df_desistencias, how='left', left_on='CD_UF', right_on='cod_estado')

    configure_plot()
    _, ax = plt.subplots(1, figsize=(20, 15))  # Tamanho da janela

    # Intervalos na legenda de cores
    boundaries = np.linspace(0, 1, 11)  
    # Mapa de cores
    cmap = ListedColormap(['#fff5f0', '#fee0d2', '#fcbba1', '#fc9272', '#fb6a4a', '#ef3b2c', '#cb181d', '#a50f15', '#67000d', '#290106'])

    plot_map(ax, mapa, 'taxa_desistencia', cmap, "\nPercentual Desistentes (Até 201X + 4) / Ingressantes (201X)", boundaries)
    title = f"Taxa de Desistência em {sigla_curso} no Brasil (2010 - 2018)"
    plt.axis('off')
    show_map(title)

#---------------------------------Main------------------------------------

def print_table(dfzao):
    # Calcula dados de bolsas
    df_bolsas = calculate_bolsas(dfzao)
    
    # Calcula dados de desistência
    df_desistencias = dfzao.groupby('cod_estado').agg({
        'qtd_ingressantes': 'sum',
        'qtd_desistencias': 'sum',
    }).reset_index()
    df_desistencias['taxa_desistencia'] = (df_desistencias['qtd_desistencias'] / df_desistencias['qtd_ingressantes']).round(2)
    
    # Combina os dataframes
    df_final = df_bolsas.merge(df_desistencias[['cod_estado', 'taxa_desistencia']], on='cod_estado')
    
    # Adiciona nomes dos estados
    estados = {
        11: 'RO', 12: 'AC', 13: 'AM', 14: 'RR', 15: 'PA', 16: 'AP', 17: 'TO',
        21: 'MA', 22: 'PI', 23: 'CE', 24: 'RN', 25: 'PB', 26: 'PE', 27: 'AL', 28: 'SE', 29: 'BA',
        31: 'MG', 32: 'ES', 33: 'RJ', 35: 'SP',
        41: 'PR', 42: 'SC', 43: 'RS',
        50: 'MS', 51: 'MT', 52: 'GO', 53: 'DF'
    }
    df_final['Estado'] = df_final['cod_estado'].map(estados)
    
    # Seleciona e renomeia colunas
    tabela = df_final[['Estado', 'percentual_total_bolsas', 'percentual_bolsas_integrais', 'percentual_bolsas_parciais', 'taxa_desistencia']]
    tabela = tabela.rename(columns={
        'percentual_total_bolsas': 'Bolsistas/Ingressantes',
        'percentual_bolsas_integrais': 'Bolsas Integrais',
        'percentual_bolsas_parciais': 'Bolsas Parciais',
        'taxa_desistencia': 'Taxa de Desistência'
    })
    
    # Formata os percentuais
    for col in tabela.columns[1:]:
        tabela[col] = (tabela[col] * 100).round(1).astype(str) + '%'
    
    # Ordena por estado
    tabela = tabela.sort_values('Estado')
    
    print("\nDados por Estado:")
    print(tabela.to_string(index=False))

if __name__ == '__main__':
    # Caminho para o shapefile e o CSV
    shapefile_path = "shapefile/BR_UF_2022.shp"

    # Carregar os dados geográficos
    mapa = gpd.read_file(shapefile_path)
    # Converte a coluna 'CD_UF' para o tipo int
    mapa['CD_UF'] = mapa['CD_UF'].astype(int)

    #sigla_curso = input('Digite a sigla do curso: ')
    sigla_curso = "cic"

    dfzao = pd.read_csv(f"arquivosCSV/bolsas_vs_desist/BR/bolsas_vs_desist-2010-2018-BR-{sigla_curso.lower()}.csv",
                        delimiter=',')

    # Gera os mapas
    plot_mapa_bolsas(dfzao, mapa, sigla_curso)
    plot_mapa_desist(dfzao, mapa, sigla_curso)
    
    # Imprime a tabela de dados
    print_table(dfzao)
