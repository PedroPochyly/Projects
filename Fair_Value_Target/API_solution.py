#Biblios

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import yfinance as yf
########################################################################################################################

#funções

def calcular_dividendo_anual(df):
    df['Ano'] = df['Data Pagamento'].dt.year
    ano_atual = datetime.now().year
    anos_validos = [ano_atual - 3, ano_atual - 2, ano_atual - 1]
    df_filtrado = df[df['Ano'].isin(anos_validos)]
    return df_filtrado.groupby('Ano')['Valor'].sum()

########################################################################################################################

#Extração de dados e criação dos DF´s

dy_esperado = 0.06
Ticker_empresas = ["AURE3", "BBAS3", "CXSE3", "KLBN3", "SAPR3"]
Ticker_empresas_lower = [empresa.lower() for empresa in Ticker_empresas]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

dfs_empresas = {}

for empresa in Ticker_empresas_lower:
    url = f"https://statusinvest.com.br/acoes/{empresa}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
   
    soup = BeautifulSoup(response.text, 'html.parser')
    tabela = soup.find("table")

    dados = [
        [coluna.text.strip() for coluna in linha.find_all("td")]
        for linha in tabela.find_all("tr")
        if linha.find_all("td")
    ]

    df_empresa = pd.DataFrame(dados, columns=["Tipo", "Data Com", "Data Pagamento", "Valor"])
########################################################################################################################
  
   #Lipar Dados

    for col in df_empresa.select_dtypes(include='object').columns:
        df_empresa[col] = df_empresa[col].str.strip()
  
    df_empresa["Valor"] = df_empresa["Valor"].apply(
        lambda x: float(re.search(r"[\d,\.]+", x).group().replace(",", ".")) if isinstance(x, str) and re.search(r"[\d,\.]+", x) else None
    )
    df_empresa["Data Pagamento"] = pd.to_datetime(df_empresa["Data Pagamento"], format="%d/%m/%Y", errors='coerce')
    df_empresa.drop("Data Com", axis=1, inplace=True)
    dfs_empresas[empresa.upper()] = df_empresa

    print(f'a {empresa} teve os seguintes rendimentos:{df_empresa}')
########################################################################################################################
   
    #calculos

    dividendos_anuais = calcular_dividendo_anual(df_empresa)
    media_3anos = dividendos_anuais.mean()
    preco_teto = media_3anos / dy_esperado if media_3anos else 0

    ticker = yf.Ticker(f"{empresa.upper()}.SA")
    cotacao_atual = ticker.fast_info["lastPrice"]
    upside = preco_teto / cotacao_atual if cotacao_atual else 0

    print(f"A média dos últimos 3 anos da empresa {empresa.upper()} é: R$ {media_3anos:.2f}")
    print(f"Preço teto (DY desejado {dy_esperado*100:.0f}%): R$ {preco_teto:.2f}")
    print(f"Cotação atual: R$ {cotacao_atual:.2f} ➜ Upside estimado: {(upside - 1) * 100:.2f}%\n")