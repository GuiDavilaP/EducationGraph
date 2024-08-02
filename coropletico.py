import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# Caminho para o Shapefile
shapefile_path = "shapefile/BR_UF_2022.shp"

# Caminho para o CSV
csv_path = "arquivosCSV/teste/bolsas_vs_desist-2011-BR.csv"

# Carregar os dados geográficos
mapa = gpd.read_file(shapefile_path)

# Carregar os dados CSV
dados = pd.read_csv(csv_path, delimiter=';')

# Verificar as primeiras linhas do CSV para garantir que os nomes das colunas estão corretos
print(dados.head())

# Calcular a média das porcentagens de bolsas por estado
media_por_estado = dados.groupby('cod_estado')['percentual_bolsas'].mean().reset_index()
media_por_estado.rename(columns={'percentual_bolsas': 'media_por_estado'}, inplace=True)

# Converter para int para garantir que os tipos de dados sejam compatíveis
mapa['CD_UF'] = mapa['CD_UF'].astype(int)
media_por_estado['cod_estado'] = media_por_estado['cod_estado'].astype(int)

# Mesclar os dados geográficos com os dados de média por estado
mapa = mapa.merge(media_por_estado, left_on="CD_UF", right_on="cod_estado")

# Verificar as colunas disponíveis no DataFrame 'mapa'
print("Colunas disponíveis no DataFrame 'mapa':", mapa.columns)

# Criar o mapa coroplético
fig, ax = plt.subplots(1, 1, figsize=(10, 6))
mapa.plot(column="media_por_estado", ax=ax, legend=True,
          legend_kwds={'label': "Média das Porcentagens de Bolsas",
                       'orientation': "horizontal"},
          cmap='OrRd')

# Adicionar título e mostrar o mapa
plt.title("Mapa Coroplético da Média das Porcentagens de Bolsas por Estado")
plt.show()