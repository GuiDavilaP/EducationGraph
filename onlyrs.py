import pandas as pd
import numpy as np

codigos_instituicao = [
    12, 13, 14, 18, 20, 21, 23, 294, 295, 296, 423, 426, 446, 448, 449, 454, 532, 581, 582, 601, 626, 631, 634, 641, 
    717, 1041, 1084, 1085, 1175, 1231, 1327, 1382, 1427, 1578, 1607, 1636, 1780, 1830, 1842, 1864, 1932, 1969, 2084, 2113, 
    2184, 2191, 2192, 2194, 2198, 2287, 2297, 2346, 2383, 2478, 2486, 2488, 2647, 2687, 2821, 2826, 2855, 2895, 2950, 3171, 
    3306, 3333, 3336, 3339, 3443, 3523, 3538, 3541, 3543, 3596, 3697, 3699, 3768, 3804, 3878, 4006, 4008, 4010, 4077, 4096, 
    4097, 4098, 4107, 4261, 4443, 4616, 4632, 4633, 4810, 4902, 5023, 5107, 5285, 5317, 5322, 5523, 5600, 11429, 12338, 12784, 15121
]

# Ler o CSV
df = pd.read_csv('arquivosCSV/prouni2010.csv',  encoding='cp1252', on_bad_lines='warn', delimiter=';')



# Filtrar o DataFrame para conter apenas os registros com CODIGO_EMEC_IES_BOLSA pertencente aos códigos de instituição
df_filtrado = df[df['CODIGO_EMEC_IES_BOLSA'].isin(codigos_instituicao)]

# Salvar o novo CSV
df_filtrado.to_csv('arquivosCSV/prouni2010RS.csv', encoding='cp1252', sep=';')

