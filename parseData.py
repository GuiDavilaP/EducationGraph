import pandas as pd
import unidecode as uni

COD_ESTADOS = {'RO': 11, 'AC': 12, 'AM': 13, 'RR': 14, 'PA': 15, 'AP': 16, 'TO': 17, 'MA': 21, 'PI': 22, 'CE': 23,
               'RN': 24, 'PB': 25, 'PE': 26, 'AL': 27, 'SE': 28, 'BA': 29, 'MG': 31, 'ES': 32, 'RJ': 33, 'SP': 35,
               'PR': 41, 'SC': 42, 'RS': 43, 'MS': 50, 'MT': 51, 'GO': 52, 'DF': 53}


def convert_to_int(value):
    if '.' in value:
        value = value.split('.')[0]
    return int(value)


def parse_data(ano_ingresso, curso):
    ano_final = ano_ingresso + 4  # 4 anos é o tempo médio de um curso de Ciência da Computação no Brasil.

    colunas_relevantes = ['Nome da Instituição', 'Nome do Curso de Graduação',
                          'Código da Unidade Federativa do Curso',
                          'Nome da área do Curso segundo a classificação CINE BRASIL',
                          'Nome da Grande Área do Curso segundo a classificação CINE BRASIL',
                          'Quantidade de Ingressantes no Curso',
                          'Taxa de Desistência Acumulada - TDA', 'Código do Curso de Graduação']

    # Lê csv: função lambda converte valores para lowercase.
    try:
        prouni = pd.read_csv(f'arquivosCSV/prouni/prouni{ano_ingresso}.csv', encoding='cp1252', on_bad_lines='warn',
                             delimiter=';').apply(lambda x: x.astype(str).str.lower())
    except UnicodeDecodeError:
        prouni = pd.read_csv(f'arquivosCSV/prouni/prouni{ano_ingresso}.csv', encoding='utf-8', on_bad_lines='warn',
                             delimiter=';').apply(lambda x: x.astype(str).str.lower())

    # Filtra bolsas presenciais.
    prouni = prouni[prouni['MODALIDADE_ENSINO_BOLSA'] == 'presencial']

    # Renomeia por conveniência no merge.
    prouni = prouni.rename(
        columns={'NOME_IES_BOLSA': 'Nome da Instituição', 'NOME_CURSO_BOLSA': 'Nome do Curso de Graduação'})

    # Adiciona colunas para cada tipo de bolsa
    prouni['qtd_bolsas_parciais'] = prouni['TIPO_BOLSA'].apply(lambda x: 1 if x == 'bolsa parcial 50%' else 0)
    prouni['qtd_bolsas_integrais'] = prouni['TIPO_BOLSA'].apply(lambda x: 1 if x == 'bolsa integral' else 0)

    # Filtra as colunas relevantes
    prouni = prouni.loc[:, colunas_relevantes[:2] + ['qtd_bolsas_parciais', 'qtd_bolsas_integrais']]

    # Agrupa por universidade e curso e soma a quantia de bolsas parciais e integrais, respectivamente.
    prouni = prouni.groupby(['Nome da Instituição', 'Nome do Curso de Graduação']).agg({
        'qtd_bolsas_parciais': 'sum',
        'qtd_bolsas_integrais': 'sum'
    }).reset_index()

    # Filtra por curso
    prouni = prouni[prouni['Nome do Curso de Graduação'].str.contains(curso.lower())]

    # Lê csv: função lambda converte valores para lowercase.
    fluxo = pd.read_csv(f'arquivosCSV/fluxo/fluxo{ano_ingresso}.csv', encoding='cp1252', on_bad_lines='warn',
                        delimiter=';',
                        ).apply(lambda x: x.astype(str).str.lower())

    # Filtra por curso
    fluxo = fluxo[fluxo['Nome do Curso de Graduação'].str.contains(curso.lower())]

    # Filtro por valores (RS, Privadas, Presencial)
    fluxo = fluxo[
        (fluxo['Categoria Administrativa'].isin(['4', '5', '7'])) &
        (fluxo['Modalidade de Ensino'].isin(['1'])) &
        (fluxo['Ano de Referência'] == str(ano_final))]

    # Filtro por colunas
    fluxo = fluxo[colunas_relevantes]

    # Conversões
    fluxo = fluxo.assign(
        **{
            'Quantidade de Ingressantes no Curso': fluxo['Quantidade de Ingressantes no Curso'].astype(int),
            'Taxa de Desistência Acumulada - TDA': fluxo['Taxa de Desistência Acumulada - TDA'].str.replace(',',
                                                                                                            '.').astype(
                float),
            'Código da Unidade Federativa do Curso': fluxo['Código da Unidade Federativa do Curso'].str.replace('.0',
                                                                                                                '').astype(int)
        }
    )

    # Cria nova coluna com quantidade de desistências.
    fluxo['Quantidade de Desistências'] = (
            fluxo['Quantidade de Ingressantes no Curso'] * fluxo[
        'Taxa de Desistência Acumulada - TDA'] / 100).round().astype(int)

    # Agrupa por universidade e curso, soma a quantia de ingressantes e quantidade de desistências.
    fluxo = fluxo.groupby(['Nome da Instituição', 'Nome do Curso de Graduação']).agg({
        'Código da Unidade Federativa do Curso': 'first',
        'Quantidade de Ingressantes no Curso': 'sum',
        'Quantidade de Desistências': 'sum',
        'Nome da Grande Área do Curso segundo a classificação CINE BRASIL': 'first',
    }).reset_index()

    #--------------------------------------------------------------------------------------------------------------------------------------#

    # Cria dataframe dfFinal a partir do dataframe prouni
    dfFinal = prouni.copy()

    # Agrupa por universidade e curso
    dfFinal = dfFinal.groupby(['Nome da Instituição', 'Nome do Curso de Graduação']).sum().reset_index()

    # Associa o nome da universidade e do curso de ambos dataframes para fazer a união
    dfFinal = pd.merge(dfFinal, fluxo[['Nome da Instituição', 'Nome do Curso de Graduação',
                                       'Código da Unidade Federativa do Curso',
                                       'Quantidade de Ingressantes no Curso',
                                       'Quantidade de Desistências',
                                       'Nome da Grande Área do Curso segundo a classificação CINE BRASIL']],
                       on=['Nome da Instituição', 'Nome do Curso de Graduação'])

    dfFinal['Quantidade Total de Bolsas'] = dfFinal['qtd_bolsas_parciais'] + dfFinal['qtd_bolsas_integrais']

    dfFinal['Percentual Total de Bolsas'] = (dfFinal['Quantidade Total de Bolsas'] / dfFinal[
        'Quantidade de Ingressantes no Curso'].sum() * 100).round(2).astype(float)

    # Se a quantidade de bolsas for maior que a quantia de ingressantes, remove a linha
    dfFinal = dfFinal[dfFinal['Quantidade Total de Bolsas'] <= dfFinal['Quantidade de Ingressantes no Curso']]

    # Calcula percentual de bolsas parciais ofertadas em relação à quantidade total de bolsas
    dfFinal['Percentual de Bolsas Parciais'] = (
            dfFinal['qtd_bolsas_parciais'] / dfFinal['Quantidade Total de Bolsas'] * 100).round(2).astype(float)

    # Calcula percentual de bolsas integrais ofertadas em relação à quantidade total de bolsas
    dfFinal['Percentual de Bolsas Integrais'] = (
            dfFinal['qtd_bolsas_integrais'] / dfFinal['Quantidade Total de Bolsas'] * 100).round(2).astype(float)

    # Calcula o percentual de desistência acumulada em relação à quantia de ingressantes no ano de ingresso.
    dfFinal['Taxa de Desistência Acumulada'] = (
            dfFinal['Quantidade de Desistências'] / dfFinal['Quantidade de Ingressantes no Curso'] * 100).round(
        2).astype(
        float)

    # Remove acentos
    dfFinal = dfFinal.map(lambda x: uni.unidecode(x) if type(x) == str else x)
    dfFinal = dfFinal.rename(columns={
        'Nome da Instituição': 'instituicao',
        'Nome do Curso de Graduação': 'curso',
        'Código da Unidade Federativa do Curso': 'cod_estado',
        'Quantidade de Ingressantes no Curso': 'qtd_ingressantes',
        'Quantidade de Desistências': 'qtd_desistencias',
        'Nome da Grande Área do Curso segundo a classificação CINE BRASIL': 'grande_area',
        'Percentual de Bolsas Parciais': 'percentual_bolsas_parciais',
        'Percentual de Bolsas Integrais': 'percentual_bolsas_integrais',
        'Taxa de Desistência Acumulada': 'taxa_desistencia_acumulada',
        'Quantidade Total de Bolsas': 'qtd_total_bolsas',
        'Percentual Total de Bolsas': 'percentual_total_bolsas'
    })

    dfFinal.to_csv(f'arquivosCSV/bolsas_vs_desist/BR/bolsas_vs_desist-{ano_ingresso}-BR-cic.csv', encoding='cp1252',
                   sep=';')


if __name__ == '__main__':
    anos = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]

    dfs = []

    for ano in anos:
        #parse_data(ano, 'Ciência Da Computação')
        dfs.append(pd.read_csv(f'arquivosCSV/bolsas_vs_desist/BR/bolsas_vs_desist-{ano}-BR-cic.csv', delimiter=';', index_col=False))
        print(f'Arquivo {ano} processado.')

    dfzao = pd.concat(dfs)

    dfzao = dfzao.groupby('instituicao').agg({
        'qtd_bolsas_parciais': 'sum',
        'qtd_bolsas_integrais': 'sum',
        'cod_estado': 'first',
        'qtd_ingressantes': 'sum',
        'grande_area': 'first',
        'qtd_desistencias': 'sum',
        'qtd_total_bolsas': 'sum',
    }).reset_index(drop=True)

    dfzao['percentual_bolsas_parciais'] = (dfzao['qtd_bolsas_parciais'] / dfzao['qtd_total_bolsas'] * 100).round(2)
    dfzao['percentual_bolsas_integrais'] = (dfzao['qtd_bolsas_integrais'] / dfzao['qtd_total_bolsas'] * 100).round(2)
    dfzao['percentual_total_bolsas'] = (dfzao['qtd_total_bolsas'] / dfzao['qtd_ingressantes'] * 100).round(2)
    dfzao['taxa_desistencia_acumulada'] = (dfzao['qtd_desistencias'] / dfzao['qtd_ingressantes'] * 100).round(2)

    dfzao = dfzao.sort_values(by='cod_estado', ascending=True)


    dfzao.to_csv(f'arquivosCSV/bolsas_vs_desist/BR/bolsas_vs_desist-2010-2018-BR-cic.csv', encoding='cp1252')

