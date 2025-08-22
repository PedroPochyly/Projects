# Primeiro, instale a biblioteca se ainda não tiver:
# pip install yfinance

import yfinance as yf
import pandas as pd

# Lista de tickers
tickers = tickers = [
    "ITUB4.SA", "BBDC3.SA", "BBAS3.SA", "SANB11.SA", "BRSR6.SA", "BBDC4.SA", "BPAC11.SA",
    "PETR3.SA", "RENT3.SA", "PRIO3.SA", "ENAT3.SA", "BRKM5.SA", "VBBR3.SA",
    "VALE3.SA", "CSNA3.SA", "GGBR4.SA", "USIM5.SA", "GOAU4.SA",
    "MGLU3.SA", "LREN3.SA", "AMER3.SA", "PCAR3.SA", "HGTX3.SA", "GUAR3.SA", "CEAB3.SA", "VVAR3.SA",
    "NEOE3.SA", "ELET3.SA", "CPLE6.SA", "ENGI11.SA", "TRPL4.SA", "CMIG4.SA", "TAEE11.SA", "ELPL3.SA", "AESB3.SA",
    "SBSP3.SA", "SAPR11.SA", "CTSA3.SA", "AMBP3.SA", "CSMG3.SA", "CASN4.SA", "ORVR3.SA",
    "VIVT3.SA", "TIMS3.SA", "OIBR3.SA",
    "JBSS3.SA", "BRFS3.SA", "ABEV3.SA", "MRFG3.SA", "MDIA3.SA"
]

# Baixar dados históricos (por exemplo, últimos 5 anos)
data = yf.download(tickers, start="2018-01-01", end="2025-01-01")['Adj Close']

# Exibir os dados
print(data)

