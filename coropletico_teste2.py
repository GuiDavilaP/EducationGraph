import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import geopandas as gpd

COD_ESTADOS = {'RO': 11, 'AC': 12, 'AM': 13, 'RR': 14, 'PA': 15, 'AP': 16, 'TO': 17, 'MA': 21, 'PI': 22, 'CE': 23,
               'RN': 24, 'PB': 25, 'PE': 26, 'AL': 27, 'SE': 28, 'BA': 29, 'MG': 31, 'ES': 32, 'RJ': 33, 'SP': 35,
               'PR': 41, 'SC': 42, 'RS': 43, 'MS': 50, 'MT': 51, 'GO': 52, 'DF': 53}

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

    # Carregar o shapefile para calcular os centroides
    shapefile_path = "shapefile/BR_UF_2022.shp"  # Substitua pelo caminho correto
    geo_df = gpd.read_file(shapefile_path)

    # Reprojetar para um CRS adequado para cálculos de área/distância
    geo_df = geo_df.to_crs(epsg=3857)

    # Calcular os centroides dos estados
    geo_df['centroid'] = geo_df.geometry.centroid
    geo_df['lat'] = geo_df.centroid.y
    geo_df['lon'] = geo_df.centroid.x

    # Normalizar as coordenadas para o intervalo [0, 1]
    min_lon, max_lon = geo_df['lon'].min(), geo_df['lon'].max()
    min_lat, max_lat = geo_df['lat'].min(), geo_df['lat'].max()

    geo_df['x_norm'] = (geo_df['lon'] - min_lon) / (max_lon - min_lon)
    geo_df['y_norm'] = (geo_df['lat'] - min_lat) / (max_lat - min_lat)

    # Mapear os códigos dos estados para suas coordenadas de centroide normalizadas
    geo_df['CD_UF'] = geo_df['CD_UF'].astype(int)  # Garantir que o código do estado seja int
    centroid_map = geo_df.set_index('CD_UF')[['x_norm', 'y_norm']].to_dict('index')

    pio.renderers.default = 'browser'

    estados_br = json.load(open('data/brazil-states.geojson', 'r'))

    # Criar o mapa coroplético de bolsas
    fig = px.choropleth(df_bolsas,
                        locations='cod_estado',
                        geojson=estados_br,
                        color='percentual_total_bolsas',
                        featureidkey="properties.codigo_ibg",
                        projection="mercator")

    # Atualizar o layout do mapa
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(title_text='Mapa Coroplético - Porcentagens de bolsas por estado')

    # Adicionar gráficos de pizza para cada estado
    for index, row in df_bolsas.iterrows():
        estado = int(row['cod_estado'])  # Garantir que o código seja int
        percentual_parciais = row['percentual_bolsas_parciais']
        percentual_integrais = row['percentual_bolsas_integrais']

        # Obter as coordenadas normalizadas do centroide
        x = centroid_map[estado]['x_norm']
        y = centroid_map[estado]['y_norm']

        # Ajustar para garantir que x e y fiquem dentro de [0, 1]
        x_min = max(x - 0.05, 0)
        x_max = min(x + 0.05, 1)
        y_min = max(y - 0.05, 0)
        y_max = min(y + 0.05, 1)

        # Adicionar gráfico de pizza
        fig.add_trace(go.Pie(
            values=[percentual_parciais, percentual_integrais],
            labels=['Bolsas Parciais', 'Bolsas Integrais'],
            hole=.3,  # Criar gráfico de pizza "donut"
            marker=dict(colors=['lightblue', 'lightgreen']),
            textinfo='none',  # Remove o texto dentro do gráfico
            showlegend=False,
            domain=dict(x=[x_min, x_max], y=[y_min, y_max]),  # Ajuste conforme necessário
            name=f"Estado {estado}"
        ))

    # Mostrar o mapa com os gráficos de pizza
    fig.show()
