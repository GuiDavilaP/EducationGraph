import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Read the CSV file
df = pd.read_csv('arquivosCSV/bolsasDesist2010RS.csv', delimiter=";", encoding='cp1252')

# Filter the dataframe for the specified course
# selected_course = "ciências econômicas"
# filtered_df = df[df['Nome do Curso de Graduação'] == selected_course]

# Filter the dataframe for the specified área do Curso segundo a classificação CINE BRASIL
selected_area = "ciências naturais, matemática e estatística"
filtered_df = df[df['Nome da Grande Área do Curso segundo a classificação CINE BRASIL'] == selected_area]

# Convert 'BOLSAS' and 'TODA' columns to numeric
filtered_df['Percentual de Bolsas'] = filtered_df['Percentual de Bolsas'].astype(float)
filtered_df['Taxa de Desistência Acumulada - TODA'] = filtered_df['Taxa de Desistência Acumulada - TODA'].str.replace(
    ',', '.').astype(float)

filtered_df.insert(2, column='Count', value=1.0)
filtered_df = filtered_df.groupby(['Nome da Instituição']).sum().reset_index()
filtered_df['Percentual de Bolsas'] = (
            filtered_df['Quantia de Bolsas'] / filtered_df['Quantidade de Ingressantes no Curso'] * 100).round(
    2).astype(float)
filtered_df['Taxa de Desistência Acumulada - TODA'] = (
            filtered_df['Taxa de Desistência Acumulada - TODA'].astype(float) / filtered_df['Count']).round(2).astype(
    float)

filtered_df.to_csv('arquivosCSV/teste.csv', encoding='cp1252', sep=';')

# Plot the graph
plt.figure(figsize=(10, 6))
for university, data in filtered_df.groupby('Nome da Instituição'):
    plt.scatter(data['Percentual de Bolsas'], data['Taxa de Desistência Acumulada - TODA'], marker='o', color='blue')

# Tentativa de fazer um cálculo da correlação de Peterson.
# correlation = np.corrcoef([filtered_df['Percentual de Bolsas'], filtered_df['Taxa de Desistência Acumulada - TODA']])
# print(" Correlação Pearson: ", correlation)

# Cria reta de aproximação linear usando library seaborn, esse método utiliza uma regressão linear que pode ser customizada pelos parâmetros.
# Propriedade truncate permite delimitar área de dados, pode ser útil para ignorar cursos com taxa de desistência incongruente.
sns.regplot(x=filtered_df['Percentual de Bolsas'], y=filtered_df['Taxa de Desistência Acumulada - TODA'])

# Add title and labels
plt.title(selected_area)
plt.xlabel('Percentual Bolsas')
plt.ylabel('Percentual Desistência')

# Add legend
plt.legend()

# Show the plot
plt.grid(True)

plt.show()
