import pandas as pd
import unidecode as uni

COD_ESTADOS = {'RO': '11.0', 'AC': '12.0', 'AM': '13.0', 'RR': '14.0', 'PA': '15.0', 'AP': '16.0', 'TO': '17.0',
               'MA': '21.0', 'PI': '22.0', 'CE': '23.0', 'RN': '24.0', 'PB': '25.0', 'PE': '26.0', 'AL': '27.0',
               'SE': '28.0', 'BA': '29.0', 'MG': '31.0', 'ES': '32.0', 'RJ': '33.0', 'SP': '35.0', 'PR': '41.0',
               'SC': '42.0', 'RS': '43.0', 'MS': '50.0', 'MT': '51.0', 'GO': '52.0', 'DF': '53.0'}
ANO = '2010'

colunas_relevantes = ['Nome da Instituição', 'Nome do Curso de Graduação',
                      'Nome da área do Curso segundo a classificação CINE BRASIL',
                      'Nome da Grande Área do Curso segundo a classificação CINE BRASIL',
                      'Quantidade de Ingressantes no Curso',
                      'Taxa de Desistência Acumulada - TDA', 'Código do Curso de Graduação']

# Lê csv: função lambda converte valores para lowercase.
prouni = pd.read_csv(f'arquivosCSV/prouni/prouni{ANO}.csv', encoding='cp1252', on_bad_lines='warn',
                     delimiter=';').apply(
    lambda x: x.astype(str).str.lower())

# Filtra bolsas presenciais.
prouni = prouni[prouni['MODALIDADE_ENSINO_BOLSA'] == 'presencial']

# Renomeia por conveniência no merge.
prouni = prouni.rename(
    columns={'NOME_IES_BOLSA': 'Nome da Instituição', 'NOME_CURSO_BOLSA': 'Nome do Curso de Graduação'})

# Filtra as colunas relevantes
prouni = prouni.loc[:, colunas_relevantes[:2]]

# Lê csv: função lambda converte valores para lowercase.
fluxo = pd.read_csv('arquivosCSV/fluxo/fluxo2010.csv', encoding='cp1252', on_bad_lines='warn', delimiter=';',
                    ).apply(lambda x: x.astype(str).str.lower())

# Filtra universidades do RS.
fluxo = fluxo[fluxo['Código da Unidade Federativa do Curso'] == COD_ESTADOS['RS']]

# Filtra as colunas relevantes
fluxo = fluxo.loc[:, colunas_relevantes]

# Converte quantidade de ingressantes para int para ser somado depois.
fluxo['Quantidade de Ingressantes no Curso'] = fluxo['Quantidade de Ingressantes no Curso'].astype(int)
# Converte taxa de desistência para float.
fluxo['Taxa de Desistência Acumulada - TDA'] = fluxo['Taxa de Desistência Acumulada - TDA'].str.replace(',',
                                                                                                        '.').astype(
    float)

# Cria nova coluna com quantidade de desistências.
fluxo['Quantidade de Desistências'] = (
        fluxo['Quantidade de Ingressantes no Curso'] * fluxo[
    'Taxa de Desistência Acumulada - TDA'] / 100).round().astype(int)

# Agrupa por universidade e curso, soma a quantia de ingressantes e quantidade de desistências.
fluxo = fluxo.groupby(['Nome da Instituição', 'Nome do Curso de Graduação']).agg({
    'Quantidade de Ingressantes no Curso': 'sum',  # Soma de ingressantes.
    'Quantidade de Desistências': 'sum',  # Soma de desistências.
    'Código do Curso de Graduação': 'first',
    'Nome da Grande Área do Curso segundo a classificação CINE BRASIL': 'first',
}).reset_index()

#--------------------------------------------------------------------------------------------------------------------------------------#

# Cria dataframe dfFinal a partir do dataframe prouni
dfFinal = prouni.copy()

# Cria coluna "Quantia de Bolsas", agrupa bolsas de uma mesma universidade e curso e conta quantia delas.
dfFinal.insert(2, column='Quantia de Bolsas', value=1)
dfFinal = dfFinal.groupby(['Nome da Instituição', 'Nome do Curso de Graduação']).sum().reset_index()

# Une a base dfFinal, que contém quantia de bolsas, com a quantidade de desistência acumulada, código do curso e quantia de ingressantes do curso, do dataframe 'fluxo'.
# Associa o nome da universidade e do curso de ambos dataframes para fazer a união
dfFinal = pd.merge(dfFinal, fluxo[['Nome da Instituição', 'Nome do Curso de Graduação',
                                   'Quantidade de Ingressantes no Curso',
                                   'Quantidade de Desistências',
                                   'Nome da Grande Área do Curso segundo a classificação CINE BRASIL']],
                   on=['Nome da Instituição', 'Nome do Curso de Graduação'])

# Se a quantidade de bolsas for maior que a quantia de ingressantes, remove a linha
dfFinal = dfFinal[dfFinal['Quantia de Bolsas'] <= dfFinal['Quantidade de Ingressantes no Curso']]

# Calcula percentual de bolsas ofertadas em relação à quantia de ingressantes.
dfFinal['Percentual de Bolsas'] = (
        dfFinal['Quantia de Bolsas'] / dfFinal['Quantidade de Ingressantes no Curso'] * 100).round(2).astype(float)

# Calcula o percentual de desistência acumulada em relação à quantia de ingressantes no ano de ingresso.
dfFinal['Taxa de Desistência Acumulada'] = (
        dfFinal['Quantidade de Desistências'] / dfFinal['Quantidade de Ingressantes no Curso'] * 100).round(2).astype(
    float)

dfFinal = dfFinal.map(lambda x: uni.unidecode(x) if type(x) == str else x)

dfFinal.to_csv(f'arquivosCSV/bolsas_vs_desist/bolsas_vs_desist-{ANO}-RS.csv', encoding='cp1252', sep=';')
