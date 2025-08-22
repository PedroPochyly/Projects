import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# ------------------------------
# Função para formatar os números em milhões/bilhões
# ------------------------------
def fmt_vendas(x):
    if x >= 1000:          
        return f'{x/1000:.1f} bilhões'
    elif x >= 1:           
        return f'{x:.1f} milhões'
    elif x > 0:            
        return f'{x*1000:.0f} mil'
    else:
        return '0'

# ------------------------------
# Carregando os dados
# ------------------------------
df = pd.read_csv("vgsales.csv")
df.dropna(inplace=True)

# ------------------------------
# Preparando dados
# ------------------------------
# Participação dos mercados
global_sales = df['Global_Sales'].sum()
lista_paises = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']

market_shares = [df[pais].sum() / global_sales for pais in lista_paises]
df_mkt_share = pd.DataFrame({
    'Região': lista_paises,
    'Market Share': market_shares
})

# Vendas por gênero
df_vendas_por_genero = (
    df.groupby("Genre")["Global_Sales"].sum()
    .sort_values(ascending=False)
    .reset_index()
)

# Vendas por plataforma
df_vendas_por_plataforma = (
    df.groupby("Platform")["Global_Sales"].sum()
    .sort_values(ascending=False)
    .reset_index()
)

# Transformando colunas de países em linhas
df_long = df.melt(
    id_vars=['Genre', 'Platform'],   
    value_vars=['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales'],  
    var_name='Country', 
    value_name='Sales'
)

# Vendas por gênero e país
vendas_por_genero_pais = (
    df_long.groupby(['Country', 'Genre'])['Sales']
    .sum()
    .reset_index()
)

# Vendas por plataforma e país
vendas_por_plataforma_pais = (
    df_long.groupby(['Country', 'Platform'])['Sales']
    .sum()
    .reset_index()
)

# ------------------------------
# Criando app Dash
# ------------------------------
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard de Vendas de Jogos", style={"textAlign": "center"}),

    # Gráfico de Market Share
    dcc.Graph(
        id="grafico-market-share",
        figure=px.pie(df_mkt_share, names="Região", values="Market Share",color_discrete_sequence=px.colors.sequential.Viridis,
                      title="Participação de Mercado por Região")
    ),

    # Gráfico de Vendas Globais por Gênero
    dcc.Graph(
        id="grafico-genero",
        figure=px.bar(df_vendas_por_genero, x="Genre", y="Global_Sales",color_discrete_sequence=px.colors.sequential.Viridis,
                      title="Vendas Globais por Gênero", text_auto=True)
    ),

    # Gráfico de Vendas por Plataforma
    dcc.Graph(
        id="grafico-plataforma",
        figure=px.bar(df_vendas_por_plataforma.head(10), x="Platform", y="Global_Sales",color_discrete_sequence=px.colors.sequential.Viridis,
                      title="Top 10 Plataformas por Vendas Globais", text_auto=True)
    ),

    html.H2("Filtros Interativos", style={"marginTop": "40px"}),

    # Dropdown para escolher o país
    dcc.Dropdown(
        id="filtro-pais",
        options=[{"label": c, "value": c} for c in df_long["Country"].unique()],
        value="NA_Sales",
        clearable=False
    ),

    # Gráficos filtrados
    dcc.Graph(id="grafico-genero-pais"),
    dcc.Graph(id="grafico-plataforma-pais"),
])

# ------------------------------
# Callbacks (interatividade)
# ------------------------------
@app.callback(
    [Output("grafico-genero-pais", "figure"),
     Output("grafico-plataforma-pais", "figure")],
    [Input("filtro-pais", "value")]
)
def atualizar_graficos(pais):
    # Gênero
    df_genero = vendas_por_genero_pais[vendas_por_genero_pais["Country"] == pais]
    fig_genero = px.bar(df_genero.sort_values("Sales", ascending=False),color_discrete_sequence=px.colors.sequential.Viridis,
                        x="Genre", y="Sales", text_auto=True,
                        title=f"Vendas por Gênero - {pais}")

    # Plataforma
    df_plataforma = vendas_por_plataforma_pais[vendas_por_plataforma_pais["Country"] == pais]
    fig_plataforma = px.bar(df_plataforma.sort_values("Sales", ascending=False).head(10),
                            x="Platform", y="Sales", text_auto=True,color_discrete_sequence=px.colors.sequential.Viridis,
                            title=f"Top Plataformas por Vendas - {pais}")

    return fig_genero, fig_plataforma

# ------------------------------
# Rodar servidor
# ------------------------------
if __name__ == "__main__":
    app.run(debug=True)
