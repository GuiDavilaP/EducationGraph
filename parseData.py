import pandas as pd
import unidecode as uni

COD_ESTADOS = {'RO': '11.0', 'AC': '12.0', 'AM': '13.0', 'RR': '14.0', 'PA': '15.0', 'AP': '16.0', 'TO': '17.0',
               'MA': '21.0', 'PI': '22.0', 'CE': '23.0', 'RN': '24.0', 'PB': '25.0', 'PE': '26.0', 'AL': '27.0',
               'SE': '28.0', 'BA': '29.0', 'MG': '31.0', 'ES': '32.0', 'RJ': '33.0', 'SP': '35.0', 'PR': '41.0',
               'SC': '42.0', 'RS': '43.0', 'MS': '50.0', 'MT': '51.0', 'GO': '52.0', 'DF': '53.0'}


def parse_data(ano_ingresso, curso):
    ANO_FINAL = ano_ingresso + 7

    colunas_relevantes = ['Nome da Instituição', 'Nome do Curso de Graduação',
                          'Código da Unidade Federativa do Curso',
                          'Nome da área do Curso segundo a classificação CINE BRASIL',
                          'Nome da Grande Área do Curso segundo a classificação CINE BRASIL',
                          'Quantidade de Ingressantes no Curso',
                          'Taxa de Desistência Acumulada - TDA', 'Código do Curso de Graduação']

    # Lê csv: função lambda converte valores para lowercase.
    prouni = pd.read_csv(f'arquivosCSV/prouni/prouni{ano_ingresso}.csv', encoding='cp1252', on_bad_lines='warn',
                         delimiter=';').apply(
        lambda x: x.astype(str).str.lower())

    # Filtra bolsas presenciais.
    prouni = prouni[prouni['MODALIDADE_ENSINO_BOLSA'] == 'presencial']

    # Renomeia por conveniência no merge.
    prouni = prouni.rename(
        columns={'NOME_IES_BOLSA': 'Nome da Instituição', 'NOME_CURSO_BOLSA': 'Nome do Curso de Graduação'})

    # Filtra as colunas relevantes
    prouni = prouni.loc[:, colunas_relevantes[:2]]

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
        (fluxo['Ano de Referência'] == str(ANO_FINAL))]

    # Filtro por colunas
    fluxo = fluxo[colunas_relevantes]

    # Conversões
    fluxo = fluxo.assign(
        **{
            'Quantidade de Ingressantes no Curso': fluxo['Quantidade de Ingressantes no Curso'].astype(int),
            'Taxa de Desistência Acumulada - TDA': fluxo['Taxa de Desistência Acumulada - TDA'].str.replace(',',
                                                                                                            '.').astype(
                float)
        }
    )

    # Cria nova coluna com quantidade de desistências.
    fluxo['Quantidade de Desistências'] = (
            fluxo['Quantidade de Ingressantes no Curso'] * fluxo['Taxa de Desistência Acumulada - TDA'] / 100).round().astype(int)

    # Agrupa por universidade e curso, soma a quantia de ingressantes e quantidade de desistências.
    fluxo = fluxo.groupby(['Nome da Instituição', 'Nome do Curso de Graduação']).agg({
        'Código da Unidade Federativa do Curso': 'first',
        'Quantidade de Ingressantes no Curso': 'sum',  # Soma de ingressantes.
        'Quantidade de Desistências': 'sum',  # Soma de desistências.
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
                                       'Código da Unidade Federativa do Curso',
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
            dfFinal['Quantidade de Desistências'] / dfFinal['Quantidade de Ingressantes no Curso'] * 100).round(
        2).astype(
        float)

    # Remove acentos
    dfFinal = dfFinal.map(lambda x: uni.unidecode(x) if type(x) == str else x)
    dfFinal = dfFinal.rename(columns={
        'Nome da Instituição': 'instituicao',
        'Nome do Curso de Graduação': 'curso',
        'Código da Unidade Federativa do Curso': 'cod_estado',
        'Quantia de Bolsas': 'qtd_bolsas',
        'Quantidade de Ingressantes no Curso': 'qtd_ingressantes',
        'Quantidade de Desistências': 'qtd_desistencias',
        'Nome da Grande Área do Curso segundo a classificação CINE BRASIL': 'grande_area',
        'Percentual de Bolsas': 'percentual_bolsas',
        'Taxa de Desistência Acumulada': 'taxa_desistencia_acumulada'
    })


    dfFinal.to_csv(f'arquivosCSV/bolsas_vs_desist/BR/bolsas_vs_desist-{ano_ingresso}-BR.csv', encoding='cp1252',
                   sep=';')

    return dfFinal


if __name__ == '__main__':
    parse_data(2012, 'engenharia')
