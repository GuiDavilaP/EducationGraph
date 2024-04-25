import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Lê csv's, função lambda converte valores para lowercase.
fluxo = pd.read_csv('arquivosCSV/Fluxo2010.csv', encoding='cp1252', on_bad_lines='warn', delimiter=';', dtype={'Código da Instituição':int}).apply(lambda x: x.astype(str).str.lower())
prouni = pd.read_csv('arquivosCSV/prouni2010.csv', encoding='cp1252', on_bad_lines='warn', delimiter=';').apply(lambda x: x.astype(str).str.lower())

# Cria dataframe dfFinal a partir do dataframe prouni
# ':' indica que quero copiar todas as linhas e a tupla Nome IES e Nome do Curso são as colunas que quero copiar.
dfFinal = prouni.loc[:, ['NOME_IES_BOLSA','NOME_CURSO_BOLSA']]

# Cria coluna Bolsas, agrupa bolsas de uma mesma universidade e curso e conta quantia delas. 
dfFinal.insert(2, column = 'BOLSAS', value = 1)
dfFinal = dfFinal.groupby(['NOME_IES_BOLSA', 'NOME_CURSO_BOLSA']).count()['BOLSAS'].reset_index()

# Renomeia por conveniência no merge.
fluxo = fluxo.rename(columns={'Taxa de Desistência Acumulada - TODA':'TODA', 'Nome da Instituição':'NOME_IES_BOLSA', 
                              'Nome do Curso de Graduação':'NOME_CURSO_BOLSA', 'Código do Curso de Graduação':'COD_CURSO'})

# Une a base dfFinal que contem quantia de bolsas com o valor de 'TODA' e Código do Curso do dataframe fluxo.
# Associa o nome da universidade e do curso de ambos dataframes para fazer a união
dfFinal = pd.merge(dfFinal, fluxo[['NOME_IES_BOLSA','NOME_CURSO_BOLSA', 'TODA', 'COD_CURSO']], on=['NOME_IES_BOLSA','NOME_CURSO_BOLSA'])
dfFinal = dfFinal[['NOME_IES_BOLSA', 'COD_CURSO', 'NOME_CURSO_BOLSA', 'BOLSAS', 'TODA']]

# Print, com opção que muda display com base no tamanho do console, se ficar bugado pode comentar.
#pd.options.display.width = 0
#print(dfFinal)

dfFinal.to_csv('arquivosCSV/bolsasDesist2010.csv', encoding='cp1252', sep=';')