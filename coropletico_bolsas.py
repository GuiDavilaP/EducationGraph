import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import numpy as np

if __name__ == '__main__':
    dfzao = pd.read_csv('arquivosCSV/bolsas_vs_desist/BR/bolsas_vs_desist-2010-2018-BR-cic.csv', delimiter=',')

    # Bolsas
    df_bolsas = dfzao.groupby('cod_estado').agg({
        'qtd_ingressantes': 'sum',
        'qtd_bolsas_parciais': 'sum',
        'qtd_bolsas_integrais': 'sum',
        'qtd_total_bolsas': 'sum',
    }).reset_index()

    # Recalcula percentuais
    df_bolsas['percentual_bolsas_parciais'] = (df_bolsas['qtd_bolsas_parciais'] / df_bolsas['qtd_total_bolsas']).round(2)
    df_bolsas['percentual_bolsas_integrais'] = (df_bolsas['qtd_bolsas_integrais'] / df_bolsas['qtd_total_bolsas']).round(2)

    df_bolsas['percentual_total_bolsas'] = (df_bolsas['qtd_total_bolsas'] / df_bolsas['qtd_ingressantes']).round(2)


    # Desistências
    df_desistencias = dfzao.groupby('cod_estado').agg({
        'qtd_ingressantes': 'sum',
        'qtd_desistencias': 'sum',
    }).reset_index()

    # Recalcula taxa de desistência
    df_desistencias['taxa_desistencia'] = (df_desistencias['qtd_desistencias'] / df_desistencias['qtd_ingressantes']).round(2)


    # Caminho para o shapefile e o CSV
    shapefile_path = "shapefile/BR_UF_2022.shp"

    # Carregar os dados geográficos
    mapa = gpd.read_file(shapefile_path)
    # Converte a coluna 'CD_UF' para o tipo int
    mapa['CD_UF'] = mapa['CD_UF'].astype(int)

    # Mesclar com o GeoDataFrame
    mapa = mapa.merge(df_bolsas, how='left', left_on='CD_UF', right_on='cod_estado')

    # Ajustar o tamanho da fonte globalmente
    plt.rcParams.update({
        'font.size': 24,  # Aumenta o tamanho da fonte
        'legend.fontsize': 20,  # Aumenta o tamanho da fonte da legenda
        'axes.titlesize': 28,  # Aumenta o tamanho da fonte dos títulos
        'axes.labelsize': 24  # Aumenta o tamanho da fonte dos rótulos dos eixos
})

    # Plotar mapa coroplético
    fig, ax = plt.subplots(1, figsize=(55, 35))
    mapa.boundary.plot(ax=ax, linewidth=2)
    mapa.plot(
        column='percentual_total_bolsas',
        ax=ax,
        legend=True,
        cmap='Greens',
        legend_kwds={
            'label': "Percentual Bolsistas / Ingressantes",
            'orientation': "horizontal",
            'shrink': 0.7  # Ajuste o tamanho da legenda se necessário
        }
    )


    # Adicionar gráficos de pizza
    for idx, row in mapa.iterrows():
        # Coordenadas do centroide do estado
        x, y = row.geometry.centroid.x, row.geometry.centroid.y
        sizes = [row['percentual_bolsas_parciais'], row['percentual_bolsas_integrais']]
        # Substitui NaN por 0
        sizes = [0 if pd.isna(size) else size for size in sizes]

        # Certifica-se de que a soma dos sizes não seja zero
        if sum(sizes) == 0:
            continue

        # Tamanho do gráfico de pizza baseado na quantidade de bolsistas, com limitação para não cobrir o mapa
        if row['qtd_total_bolsas'] == 0 or pd.isna(row['qtd_total_bolsas']):
            size = 0.1  # Valor padrão se qtd_total_bolsas for 0 ou NaN
        else:
            size = min(0.8, np.log10(row['qtd_total_bolsas']) * 0.2)

        # Adiciona o gráfico de pizza
        ax.pie(sizes, radius=size, center=(x, y), colors=['lightblue', 'blue'], startangle=90, counterclock=False, wedgeprops={'edgecolor': 'gray'})

    # Configurar título e mostrar o mapa
    plt.title('Bolsistas Parciais e Integrais do ProUni em CiC no Brasil (2010 - 2018)', fontsize=64)
    plt.axis('equal')  # Mantém a proporção
    plt.show()
