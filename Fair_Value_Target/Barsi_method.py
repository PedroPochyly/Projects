from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from datetime import datetime
import yfinance as yf


tickers = ["AURE3", "BBAS3", "CXSE3", "KLBN3", "SAPR3"]

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 20)

dfs = {}

for ticker in tickers:
    print(f"\n🔍 Coletando dados de: {ticker}")
    driver.get(f'https://statusinvest.com.br/acoes/{ticker.lower()}')

    try:
        div7 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/main/div[3]/div/div[1]/div[2]/div[7]'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", div7)
        time.sleep(2)

        wait.until(EC.presence_of_element_located((
            By.XPATH, '/html/body/main/div[3]/div/div[1]/div[2]/div[7]/div/div[2]/table')))
    except:
        print(f"⚠️ Tabela de proventos não encontrada para {ticker}. Pulando...\n")
        continue

    dados = []
    pagina = 1

    while pagina <= 6:
        print(f"📄 Página {pagina}...")
        driver.execute_script("arguments[0].scrollIntoView(true);", div7)
        time.sleep(1)

        if pagina > 1:
            try:
                xpath_botao = f'//ul/li/a[text()="{pagina}"]'
                botao = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_botao)))
                driver.execute_script("arguments[0].click();", botao)
                time.sleep(1.5)
            except:
                print(f"✅ Fim da paginação para {ticker}. Última página coletada: {pagina - 1}")
                break

        linhas = driver.find_elements(By.XPATH, '/html/body/main/div[3]/div/div[1]/div[2]/div[7]/div/div[2]/table/tbody/tr')
        for linha in linhas:
            colunas = linha.find_elements(By.TAG_NAME, 'td')
            linha_dados = [c.text.strip() for c in colunas]
            if len(linha_dados) == 4:
                dados.append(linha_dados)

        pagina += 1

    df = pd.DataFrame(dados, columns=['Tipo', 'Data Com', 'Pagamento', 'Valor'])
    df = df[['Pagamento', 'Valor']]
    df['Pagamento'] = pd.to_datetime(df['Pagamento'], format='%d/%m/%Y', errors='coerce')
    df['Valor'] = (
        df['Valor']
        .str.replace(r'[^\d,]', '', regex=True)
        .str.replace(',', '.', regex=False)
        .astype(float)
    )
    df.dropna(inplace=True)
    dfs[ticker] = df

   
    df_resampled = df.resample('YE', on='Pagamento')['Valor'].sum()
    preco_teto_ano = df_resampled / 0.06

    resultado = pd.DataFrame({
        'Ano': df_resampled.index.year,
        'Dividendo Total': df_resampled.values.round(2),
        'Preço Teto (DY 6%)': preco_teto_ano.values.round(2)
    })

    print(f"\n📊 Resultado Anual de {ticker}:")
    print(resultado)

    # Calculo média dos 3 anos anteriores ao atual
    ano_atual = datetime.now().year
    anos_validos = [ano_atual - 3, ano_atual - 2, ano_atual - 1]
    base_media = resultado[resultado['Ano'].isin(anos_validos)]

    if len(base_media) == 3:
        media_3anos = base_media['Dividendo Total'].mean()
        preco_teto = media_3anos / 0.06

        yf_ticker = yf.Ticker(f"{ticker}.SA")
        try:
            preco_atual = yf_ticker.fast_info['lastPrice']
        except:
            preco_atual = None

        print(f"\n📌 Média dos dividendos ({anos_validos}): R$ {media_3anos:.2f}")
        print(f"🎯 Preço teto (DY 6%): R$ {preco_teto:.2f}")

        if preco_atual:
            upside = (preco_teto / preco_atual - 1) * 100
            print(f"💸 Cotação atual: R$ {preco_atual:.2f}")
            print(f"📈 Upside estimado: {upside:.2f}%")
        else:
            print("❌ Não foi possível obter a cotação atual.")
    else:
        print("⚠️ Dados insuficientes para calcular a média dos últimos 3 anos.")
    print("")
    print("=================================================================================================")


# Encerra navegador
driver.quit()
