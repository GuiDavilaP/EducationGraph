import numpy as np
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Lê csv's, função lambda converte valores para lowercase.
fluxo = pd.read_csv('arquivosCSV/Fluxo2010.csv', encoding='cp1252', on_bad_lines='warn', delimiter=';', dtype={'Código da Instituição':int}).apply(lambda x: x.astype(str).str.lower())
prouni = pd.read_csv('arquivosCSV/prouni2010.csv', encoding='cp1252', on_bad_lines='warn', delimiter=';').apply(lambda x: x.astype(str).str.lower())

# Cria dataframe dfFinal a partir do dataframe prouni
# ':' indica que quero copiar todas as linhas e a tupla Nome IES e Nome do Curso são as colunas que quero copiar.
dfFinal = prouni.loc[:, ['NOME_IES_BOLSA','NOME_CURSO_BOLSA']]

# Renomeia por conveniência no merge.
dfFinal = dfFinal.rename(columns = {'NOME_IES_BOLSA':'Nome da Instituição', 'NOME_CURSO_BOLSA':'Nome do Curso de Graduação'})

# Cria coluna Bolsas, agrupa bolsas de uma mesma universidade e curso e conta quantia delas. 
dfFinal.insert(2, column = 'Quantia de Bolsas', value = 1)
dfFinal = dfFinal.groupby(['Nome da Instituição', 'Nome do Curso de Graduação']).sum().reset_index()

# Soma quantia de ingressantes em mesma universidade e curso
fluxo['Quantidade de Ingressantes no Curso'] = fluxo['Quantidade de Ingressantes no Curso'].astype(int)
fluxo = fluxo.groupby(['Nome da Instituição', 'Nome do Curso de Graduação']).agg({
    'Quantidade de Ingressantes no Curso': 'sum',  # Soma de ingressantes.
    'Taxa de Desistência Acumulada - TODA': 'first',
    'Código do Curso de Graduação': 'first'
}).reset_index()

# Une a base dfFinal, que contém quantia de bolsas, com a taxa de desistência total, código do curso e quantia de ingressantes do curso, do dataframe 'fluxo'.
# Associa o nome da universidade e do curso de ambos dataframes para fazer a união
dfFinal = pd.merge(dfFinal, fluxo[['Nome da Instituição', 'Código do Curso de Graduação', 'Nome do Curso de Graduação', 'Quantidade de Ingressantes no Curso',
                                   'Taxa de Desistência Acumulada - TODA']], on=['Nome da Instituição','Nome do Curso de Graduação'])

# Calcula percentual de bolsas ofertadas em relação a quantia de ingressantes.
dfFinal['Percentual de Bolsas'] = (dfFinal['Quantia de Bolsas'] / dfFinal['Quantidade de Ingressantes no Curso'] * 100).round(2).astype(float)

# Remove colunas desnecessárias ('Quantia de Bolsas' e 'Quantidade de Ingressantes no Curso') e reordena colunas restantes.
dfFinal = dfFinal[['Nome da Instituição', 'Código do Curso de Graduação', 'Nome do Curso de Graduação',
                   'Quantia de Bolsas', 'Quantidade de Ingressantes no Curso', 'Percentual de Bolsas', 'Taxa de Desistência Acumulada - TODA']]

# Print, com opção que muda display com base no tamanho do console, se ficar bugado pode comentar.
#pd.options.display.width = 0x
#print(dfFinal)

dfFinal.to_csv('arquivosCSV/bolsasDesist2010.csv', encoding='cp1252', sep=';')
