import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import numpy as np

if __name__ == '__main__':
    # Caminho para o shapefile e o CSV
    shapefile_path = "shapefile/BR_UF_2022.shp"

    # Carregar os dados geográficos
    mapa = gpd.read_file(shapefile_path)
    # Converte a coluna 'CD_UF' para o tipo int
    mapa['CD_UF'] = mapa['CD_UF'].astype(int)

    curso = input('Digite a sigla do curso: ')

    dfzao = pd.read_csv('arquivosCSV/bolsas_vs_desist/BR/bolsas_vs_desist-2010-2018-BR-ecp.csv', delimiter=',')


    # Desistências
    df_desistencias = dfzao.groupby('cod_estado').agg({
        'qtd_ingressantes': 'sum',
        'qtd_desistencias': 'sum',
    }).reset_index()

    # Recalcula taxa de desistência
    df_desistencias['taxa_desistencia'] = (df_desistencias['qtd_desistencias'] / df_desistencias['qtd_ingressantes']).round(2)


    # Mesclar com o GeoDataFrame
    mapa = mapa.merge(df_desistencias, how='left', left_on='CD_UF', right_on='cod_estado')


    # Ajustar o tamanho da fonte globalmente
    plt.rcParams.update({
        'font.size': 50,  # Aumenta o tamanho da fonte
        'legend.fontsize': 20,  # Aumenta o tamanho da fonte da legenda
        'axes.titlesize': 28,  # Aumenta o tamanho da fonte dos títulos
        'axes.labelsize': 24  # Aumenta o tamanho da fonte dos rótulos dos eixos
    })

    # Plotar mapa coroplético
    fig, ax = plt.subplots(1, figsize=(55, 35))
    mapa.boundary.plot(ax=ax, linewidth=2)
    mapa.plot(
        column='taxa_desistencia',
        ax=ax,
        legend=True,
        cmap='Reds',
        legend_kwds={
            'label': "\nPercentual Desistentes (Até 201X + 4) / Ingressantes (201X)",
            'orientation': "horizontal",
        }
    )

    # Configurar título e mostrar o mapa
    plt.title('Taxa de Desistência em ECP no Brasil (2010 - 2018)', fontsize=64)
    plt.axis('equal')  # Mantém a proporção
    plt.show()
