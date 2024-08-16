import geopandas as gpd

# Caminho para o Shapefile
shapefile_path = "shapefile/BR_UF_2022.shp"

# Carregar os dados geográficos
mapa = gpd.read_file(shapefile_path)

# Exibir os nomes das colunas
print(mapa.columns)