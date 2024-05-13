import matplotlib.pyplot as plt
import pandas as pd

# Método utilizado no plotBigGraph que filtra o csv de acordo com o gráfico desejado.
def filterData(nomeCsv, selected, area = 0, university = "none"):
    #-------------------------------------Lê o arquivo CSV-----------------------------------------------
    df = pd.read_csv('arquivosCSV/'+nomeCsv+'.csv', delimiter=";", encoding='cp1252')

    #------------------------------------------Filtra----------------------------------------------------
    #Filtra por Curso ou Área.
    if(area == 1):
        #Filtra o dataframe pela área do Curso segundo a classificação CINE BRASIL.
        filtered_df = df[df['Nome da Grande Área do Curso segundo a classificação CINE BRASIL'] == selected]
    else:
        # Filtra pelo curso especificado.
        filtered_df = df[df['Nome do Curso de Graduação'] == selected]
    
    # Filtra pelo nome da universidade se existe.
    if(university != "none"):
        filtered_df = filtered_df[filtered_df['Nome da Instituição'] == university]

    #------------------------------------------Percentuais-------------------------------------------------
    # Convert 'BOLSAS' and 'TDA' columns to numeric
    filtered_df['Percentual de Bolsas'] = filtered_df['Percentual de Bolsas'].astype(float)

    # Calcula o percentual de bolsas e taxa de desistência final.
    filtered_df.insert(2, column = 'Count', value = 1.0)
    filtered_df.groupby(['Nome da Instituição']).sum()
    filtered_df['Percentual de Bolsas'] = (filtered_df['Quantia de Bolsas'] / filtered_df['Quantidade de Ingressantes no Curso'] * 100).round(2).astype(float)
    filtered_df['Taxa de Desistência Acumulada'] = (filtered_df['Quantidade de Desistências'] / filtered_df['Quantidade de Ingressantes no Curso'] * 100).round(2).astype(float)
    filtered_df = filtered_df.drop(columns="Unnamed: 0")

    # Arquivos de teste, salva os percentuais finais.
    #filtered_df.to_csv('arquivosCSV/teste/'+nomeCsv+'.csv', encoding='cp1252', sep=';')

    return filtered_df
