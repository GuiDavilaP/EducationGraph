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

    # ------------------------------- Código do Indiano -------------------------------- #

    pio.renderers.default = 'browser'

    estados_br = json.load(open('data/brazil-states.geojson', 'r'))

    state_id_map = {}
    for feature in estados_br['features']:
        feature['id'] = feature['properties']['codigo_ibg']
        state_id_map[feature['properties']['sigla']] = feature['id']

    print(state_id_map)

# --------------------------------------------------------------------------------- #

# # Criar o mapa coroplético desistência
# fig = px.choropleth(df_desistencias,
#                     locations='cod_estado',
#                     geojson=estados_br,
#                     color='taxa_desistencia',
#                     featureidkey="properties.codigo_ibg",
#                     projection="mercator")


# Criar o mapa coroplético bolsas
fig = px.choropleth(df_bolsas,
                    locations='cod_estado',
                    geojson=estados_br,
                    color='percentual_total_bolsas',
                    featureidkey="properties.codigo_ibg",
                    projection="mercator")

print("Checkpoint 1")

# Atualizar o layout do mapa
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(title_text='Mapa Coroplético - Porcentagens de bolsas por estado')

print("Checkpoint 2")

# Mostrar o mapa
fig.show()
