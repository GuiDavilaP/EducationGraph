import json
import pandas as pd
import plotly.express as px
import plotly.io as pio

COD_ESTADOS = {'RO': 11, 'AC': 12, 'AM': 13, 'RR': 14, 'PA': 15, 'AP': 16, 'TO': 17, 'MA': 21, 'PI': 22, 'CE': 23,
               'RN': 24, 'PB': 25, 'PE': 26, 'AL': 27, 'SE': 28, 'BA': 29, 'MG': 31, 'ES': 32, 'RJ': 33, 'SP': 35,
               'PR': 41, 'SC': 42, 'RS': 43, 'MS': 50, 'MT': 51, 'GO': 52, 'DF': 53}

if __name__ == '__main__':
    dfzao = pd.read_csv('arquivosCSV/bolsas_vs_desist/BR/bolsas_vs_desist-2010-2018-BR-cic.csv', delimiter=',')

    # Bolsas
    df_bolsas = dfzao.groupby('cod_estado').agg({
        'qtd_total_bolsas': lambda x: round(x.mean(), 2),
        'percentual_bolsas_parciais': lambda x: round(x.mean(), 2),
        'percentual_bolsas_integrais': lambda x: round(x.mean(), 2),
    }).reset_index()

    df_bolsas = df_bolsas.rename(columns={
        'qtd_total_bolsas': 'media_total_bolsas',
        'percentual_bolsas_parciais': 'media_percentual_bolsas_parciais',
        'percentual_bolsas_integrais': 'media_percentual_bolsas_integrais'
    })

    # Desistências
    df_desistencias = dfzao.groupby('cod_estado').agg({
        'qtd_ingressantes': lambda x: round(x.mean(), 2),
        'taxa_desistencia_acumulada': lambda x: round(x.mean(), 2),
        'qtd_desistencias': lambda x: round(x.mean(), 2),
    }).reset_index()

    df_desistencias = df_desistencias.rename(columns={
        'qtd_ingressantes': 'media_ingressantes',
        'taxa_desistencia_acumulada': 'media_taxa_desistencia_acumulada',
        'qtd_desistencias': 'media_desistencias'
    })

    # ------------------------------- Código do Indiano -------------------------------- #

    pio.renderers.default = 'browser'

    estados_br = json.load(open('data/brazil-states.geojson', 'r'))

    state_id_map = {}
    for feature in estados_br['features']:
        feature['id'] = feature['properties']['codigo_ibg']
        state_id_map[feature['properties']['sigla']] = feature['id']

    print(state_id_map)

# --------------------------------------------------------------------------------- #

# Criar o mapa coroplético
fig = px.choropleth(df_bolsas,
                    locations='cod_estado',
                    geojson=estados_br,
                    color='media_total_bolsas',
                    featureidkey="properties.codigo_ibg",
                    projection="mercator")

print("Checkpoint 1")

# Atualizar o layout do mapa
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(title_text='Mapa Coroplético - Média de Bolsas por Estado')

print("Checkpoint 2")

# Mostrar o mapa
fig.show()
