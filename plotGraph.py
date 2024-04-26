import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Read the CSV file
df = pd.read_csv('arquivosCSV/bolsasDesist2010reduced.csv', delimiter=";", encoding='cp1252')

# Filter the dataframe for the specified universities and course
selected_universities = ["pontifícia universidade católica do rio grande do sul",
                         "universidade de caxias do sul",
                         "universidade de passo fundo"]
selected_course = "ciência da computação"

filtered_df = df[(df['NOME_IES_BOLSA'].isin(selected_universities)) & 
                 (df['NOME_CURSO_BOLSA'] == selected_course)]

# Convert 'BOLSAS' and 'TODA' columns to numeric
filtered_df['BOLSAS'] = pd.to_numeric(filtered_df['BOLSAS'])
filtered_df['TODA'] = filtered_df['TODA'].str.replace(',', '.').astype(float)

# Define colors for each university
colors = {'pontifícia universidade católica do rio grande do sul': 'red',
          'universidade de caxias do sul': 'green',
          'universidade de passo fundo': 'blue'}

# Plot the graph with different colors for each university
plt.figure(figsize=(10, 6))
for university, data in filtered_df.groupby('NOME_IES_BOLSA'):
    plt.scatter(data['BOLSAS'], data['TODA'], marker='o', color=colors[university], label=university)

# Add title and labels
plt.title('BOLSAS vs TODA for ciência da computação')
plt.xlabel('BOLSAS')
plt.ylabel('TODA')

# Add legend
plt.legend()

# Show the plot
plt.grid(True)
plt.show()