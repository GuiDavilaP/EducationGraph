import pandas as pd


# Ler o CSV
df = pd.read_csv('arquivosCSV/bolsasDesist2010RS.csv',  encoding='cp1252', on_bad_lines='warn', delimiter=';')


# Conta o número de universidades diferentes
num_universidades = df['Nome da Instituição'].nunique()
print("Número de universidades diferentes:", num_universidades)