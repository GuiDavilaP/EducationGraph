import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Lê csv's, função lambda converte valores para lowercase.
prouni = pd.read_csv('arquivosCSV/prouni2011RS.csv', encoding='cp1252', on_bad_lines='warn', delimiter=';').apply(
    lambda x: x.astype(str).str.lower())

prouni = prouni[prouni['MODALIDADE_ENSINO_BOLSA'] == 'presencial']
prouni.to_csv('arquivosCSV/prouni2011RSteste.csv', encoding='cp1252', sep=';')

fluxo = pd.read_csv('arquivosCSV/fluxo2011.csv', encoding='cp1252', on_bad_lines='warn', delimiter=';', 
                    dtype={'Código da Instituição':int}).apply(lambda x: x.astype(str).str.lower())

# Selecionando as colunas relevantes
#prouni = prouni.drop('Unnamed: 0', axis=1)

colunas_relevantes = ['Nome da Instituição', 'Nome do Curso de Graduação',
                      'Nome da área do Curso segundo a classificação CINE BRASIL',
                      'Nome da Grande Área do Curso segundo a classificação CINE BRASIL',
                      'Quantidade de Ingressantes no Curso',
                      'Taxa de Desistência Acumulada - TODA', 'Código do Curso de Graduação']

for column in fluxo.columns:
    if column not in colunas_relevantes:
        fluxo = fluxo.drop(column, axis=1)

# Converte quantiade de ingressantes para int para ser somado depois.
fluxo['Quantidade de Ingressantes no Curso'] = fluxo['Quantidade de Ingressantes no Curso'].astype(int)
# Converte taxa de desistência para float.
fluxo['Taxa de Desistência Acumulada - TODA'] = fluxo['Taxa de Desistência Acumulada - TODA'].str.replace(',', '.').astype(float)

# Cria nova coluna com quantidade de desistências.
fluxo['Quantidade de Desistências'] = (fluxo['Quantidade de Ingressantes no Curso'] * fluxo['Taxa de Desistência Acumulada - TODA'] / 100).round()

# Agrupa por universidade e curso, soma a quantia de ingressantes e quantidade de desistências.
fluxo = fluxo.groupby(['Nome da Instituição', 'Nome do Curso de Graduação']).agg({
    'Quantidade de Ingressantes no Curso': 'sum',  # Soma de ingressantes.
    'Quantidade de Desistências': 'sum', # Soma de desistências.
    'Código do Curso de Graduação': 'first',
    'Nome da Grande Área do Curso segundo a classificação CINE BRASIL': 'first',
}).reset_index()

#--------------------------------------------------------------------------------------------------------------------------------------#

# Cria dataframe dfFinal a partir do dataframe prouni
# ':' indica que quero copiar todas as linhas e a tupla Nome IES e Nome do Curso são as colunas que quero copiar.
dfFinal = prouni.loc[:, ['NOME_IES_BOLSA','NOME_CURSO_BOLSA']]

# Renomeia por conveniência no merge.
dfFinal = dfFinal.rename(
    columns = {'NOME_IES_BOLSA':'Nome da Instituição', 'NOME_CURSO_BOLSA':'Nome do Curso de Graduação'})

# Cria coluna Bolsas, agrupa bolsas de uma mesma universidade e curso e conta quantia delas. 
dfFinal.insert(2, column = 'Quantia de Bolsas', value = 1)
dfFinal = dfFinal.groupby(['Nome da Instituição', 'Nome do Curso de Graduação']).sum().reset_index()

# Une a base dfFinal, que contém quantia de bolsas, com a taxa de desistência total, código do curso e quantia de ingressantes do curso, do dataframe 'fluxo'.
# Associa o nome da universidade e do curso de ambos dataframes para fazer a união
dfFinal = pd.merge(dfFinal, fluxo[['Nome da Instituição', 'Código do Curso de Graduação', 'Nome do Curso de Graduação', 'Quantidade de Ingressantes no Curso',
                                   'Quantidade de Desistências', 'Nome da Grande Área do Curso segundo a classificação CINE BRASIL']], on=['Nome da Instituição','Nome do Curso de Graduação'])

# Se a quantidade de bolsas for maior que a quantia de ingressantes, remove a linha
dfFinal = dfFinal[dfFinal['Quantia de Bolsas'] <= dfFinal['Quantidade de Ingressantes no Curso']]

# Calcula percentual de bolsas ofertadas em relação a quantia de ingressantes.
dfFinal['Percentual de Bolsas'] = (
    dfFinal['Quantia de Bolsas'] / dfFinal['Quantidade de Ingressantes no Curso'] * 100).round(2).astype(float)

# Print, com opção que muda display com base no tamanho do console, se ficar bugado pode comentar.
#pd.options.display.width = 0x
#print(dfFinal)

dfFinal.to_csv('arquivosCSV/bolsasDesist2011RS.csv', encoding='cp1252', sep=';')