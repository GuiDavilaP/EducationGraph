import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Read the CSV file
df = pd.read_csv('arquivosCSV/bolsasDesist2010.csv', delimiter=";", encoding='cp1252')

# Filter the dataframe for the specified course
selected_course = "arquitetura e urbanismo"

filtered_df = df[df['Nome do Curso de Graduação'] == selected_course]

# Convert 'BOLSAS' and 'TODA' columns to numeric
filtered_df['Percentual de Bolsas'] = filtered_df['Percentual de Bolsas'].astype(float)
filtered_df['Taxa de Desistência Acumulada - TODA'] = filtered_df['Taxa de Desistência Acumulada - TODA'].str.replace(',', '.').astype(float)

# Plot the graph
plt.figure(figsize=(10, 6))
for university, data in filtered_df.groupby('Nome da Instituição'):
    plt.scatter(data['Percentual de Bolsas'], data['Taxa de Desistência Acumulada - TODA'], marker='o', color='blue')

# Tentativa de fazer um cálculo da correlação de Peterson.
#correlation = np.corrcoef([filtered_df['Percentual de Bolsas'], filtered_df['Taxa de Desistência Acumulada - TODA']])
#print(" Correlação Pearson: ", correlation)

# Cria reta de aproximação linear usando library seaborn, esse método utiliza uma regressão linear que pode ser customizada pelos parâmetros.
# Propriedade truncate permite delimitar área de dados, pode ser útil para ignorar cursos com taxa de desistência incongruente.
sns.regplot(x = filtered_df['Percentual de Bolsas'], y = filtered_df['Taxa de Desistência Acumulada - TODA'])

# Add title and labels
plt.title(selected_course)
plt.xlabel('Percentual Bolsas')
plt.ylabel('Percentual Desistência')

# Add legend
plt.legend()

# Show the plot
plt.grid(True)

plt.show()