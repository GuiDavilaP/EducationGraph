import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Carregar o arquivo CSV
file_path = 'arquivosCSV/bolsasDesist2010.csv'
df = pd.read_csv(file_path, encoding='cp1252', sep=';')

# Lista de universidades desejadas
universidades_desejadas = [
    'universidade de caxias do sul',
    'universidade luterana do brasil',
    'pontifícia universidade católica do rio grande do sul',
    'universidade de passo fundo'
]

# Filtrar o DataFrame para incluir apenas as universidades desejadas
df_filtered = df[df['NOME_IES_BOLSA'].str.lower().isin(universidades_desejadas)]

# Salvar o DataFrame filtrado em um novo arquivo CSV
output_file_path = 'arquivosCSV/bolsasDesist2010reduced.csv'
df_filtered.to_csv(output_file_path, encoding='cp1252', sep=';', index=False)
