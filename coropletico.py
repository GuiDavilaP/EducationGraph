import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd

# Caminho para o shapefile e o CSV
shapefile_path = "shapefile/BR_UF_2022.shp"
csv_path = "arquivosCSV/bolsas_vs_desist/BR/bolsas_vs_desist-2014-BR-cic.csv"

# Carregar os dados geográficos
mapa = gpd.read_file(shapefile_path)
# Converte a coluna 'CD_UF' para o tipo int
mapa['CD_UF'] = mapa['CD_UF'].astype(int)

# Carregar e preparar os dados CSV
dados = pd.read_csv(csv_path, delimiter=';')
dados['cod_estado'] = dados['cod_estado'].astype(int)  # Garantir tipo correto

# Calcular médias de percentuais de bolsas por estado
media_bolsas = dados.groupby('cod_estado').agg({
    'percentual_bolsas_parciais': 'mean',
    'percentual_bolsas_integrais': 'mean',
    'qtd_total_bolsas': 'mean'
}).reset_index()

# Mesclar com o GeoDataFrame
mapa = mapa.merge(media_bolsas, how='left', left_on='CD_UF', right_on='cod_estado')

# Plotar mapa coroplético
fig, ax = plt.subplots(1, figsize=(10, 6))
mapa.boundary.plot(ax=ax, linewidth=1)
mapa.plot(column='percentual_bolsas_integrais', ax=ax, legend=True, cmap='OrRd')

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
        size = min(0.5, 0.1 * row['qtd_total_bolsas'])

    # Adiciona o gráfico de pizza
    ax.pie(sizes, radius=size, center=(x, y), colors=['blue', 'red'], startangle=90, counterclock=False, wedgeprops={'edgecolor': 'white'})

# Configurar título e mostrar o mapa
plt.title('Mapa Coroplético com Gráficos de Pizza das Médias de Bolsas por Estado')
plt.axis('equal')  # Mantém a proporção
plt.show()
