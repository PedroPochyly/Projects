import pandas as pd
import yfinance as yf
import requests
from bs4 import BeautifulSoup

def get_dados_status_invest(ticker_brasileiro):
    papel = ticker_brasileiro.replace(".SA", "").lower()
    headers = {"User-Agent": "Mozilla/5.0"}

    # 1. Payout médio (API)
    url_payout = f"https://statusinvest.com.br/acao/payoutresult?code={papel}"
    r = requests.get(url_payout, headers=headers)
    payout_medio = float(r.json().get("avg", 0)) / 100

    # 2. Total de ações (scraping)
    url_html = f"https://statusinvest.com.br/acoes/{papel}"
    r2 = requests.get(url_html, headers=headers)
    soup = BeautifulSoup(r2.text, "html.parser")

    for h3 in soup.find_all("h3"):
        if "total de papéis" in h3.text.lower():
            strong = h3.find_next("strong")
            num_acoes = int(strong.text.strip().replace(".", "").replace(",", ""))
            return payout_medio, num_acoes

    raise ValueError(f"Não foi possível localizar o total de papéis de {papel}")

# ✅ Lista de ações
Acoes = ["AURE3", "BBAS3", "CXSE3", "KLBN3", "SAPR3"]
Acoes = [acao + ".SA" for acao in Acoes]

for empresa in Acoes:
    payout_medio, num_acoes = get_dados_status_invest(empresa)

    ticker = yf.Ticker(empresa)
    financials = ticker.financials.T
    lucro_liquido = financials["Net Income"]

    lucro_liquido.index = pd.to_datetime(lucro_liquido.index)
    ultimos_anos = lucro_liquido[lucro_liquido.index >= pd.Timestamp.now() - pd.DateOffset(years=4)]
    ultimos_anos = ultimos_anos.sort_index()

    df = pd.DataFrame(ultimos_anos, columns=["Net Income"])
    df["Net Income"] = df["Net Income"].astype(float)
    df["Var"] = df["Net Income"].pct_change()
    var_media = df["Var"].mean()

    lucro_futuro = df["Net Income"].iloc[-1] * (1 + var_media)
    lpa = lucro_futuro / num_acoes
    dividendo_futuro = lpa * payout_medio
    preco_teto = dividendo_futuro / 0.06
    preco_atual = ticker.info["regularMarketPrice"]
    upside = ((preco_teto / preco_atual) - 1) * 100

    print(f"\n📈 {empresa}")
    print(f"🔎 Dados capturados:")
    print(f"  • Payout médio: {payout_medio:.2%}")
    print(f"  • Total de papéis: {num_acoes:,}")
    print(f"  • Preço atual: R$ {preco_atual:.2f}")
    print(f"📊 Projeções:")
    print(f"  • Crescimento médio anual do lucro: {var_media * 100:.2f}%")
    print(f"  • Lucro Futuro: R$ {lucro_futuro:,.2f}")
    print(f"  • LPA Projetado: R$ {lpa:.2f}")
    print(f"  • Dividendo Futuro: R$ {dividendo_futuro:.2f}")
    print(f"🎯 Preço Teto (Yield 6%): R$ {preco_teto:.2f}")
    print(f"🚀 Upside Potencial: {upside:.2f}%")
    print("")
    print("========================================================")


# preciso pegar o lucro líquido de todas as empresas, assim como o numero total de papeis e a média do payout

# Ver como o lucro liquido cresce e aplicar essa taxa para projetar o lucro nos proximos semestres e depois devidir pelo
# numero total de papeis do ativo, descobrindo o LPA, depois basta aplicar o payout e descobrir o dividendo por ação futuro,




