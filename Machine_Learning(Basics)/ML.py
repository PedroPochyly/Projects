import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('vgsales.csv')
df.dropna(inplace=True)

# Participação dos mercados
global_sales = df['Global_Sales'].sum()
lista_paises = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']

market_shares = [df[pais].sum() / global_sales for pais in lista_paises]

df_mkt_share = pd.DataFrame({'Região': lista_paises,
                            'Market Share': market_shares})                           
#grafico mkt_share
sns.set_style("whitegrid")
plt.figure(figsize=(10, 6))
cores_games = sns.color_palette("viridis", n_colors=len(lista_paises))
plt.pie(df_mkt_share['Market Share'], labels=df_mkt_share['Região'],colors= cores_games, autopct='%1.1f%%')


# Análise de vendas por gênero
vendas_por_genero = df.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=False)
df_vendas_por_genero = pd.DataFrame(vendas_por_genero).reset_index()
# Gráfico de vendas por gênero
plt.figure(figsize=(10, 6))
sns.barplot(x='Global_Sales', y='Genre', data=df_vendas_por_genero, palette='viridis')
plt.title('Vendas Globais por Gênero de Jogo')


# Análise de vendas por plataforma
vendas_por_plataforma = df.groupby('Platform')['Global_Sales'].sum().sort_values(ascending=False)
df_vendas_por_plataforma = pd.DataFrame(vendas_por_plataforma).reset_index()



