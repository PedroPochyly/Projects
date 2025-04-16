import pandas as pd
import yfinance as yf

Acoes = ["AURE3", "BBAS3", "CXSE3", "KLBN3", "SAPR3"]
Acoes = [acao + ".SA" for acao in Acoes]

dataframes = {}

for empresa in Acoes:
    ticker = yf.Ticker(empresa)
    financials = ticker.financials.T

    lucro_liquido = financials["Net Income"]

   
    lucro_liquido.index = pd.to_datetime(lucro_liquido.index)
    ultimos_4_anos = lucro_liquido.loc[lucro_liquido.index >= pd.Timestamp.now() - pd.DateOffset(years=4)]

    
    lucro_liquido_semestral = ultimos_4_anos.resample("6ME").sum()
    lucro_liquido_semestral = lucro_liquido_semestral.dropna()
    lucro_liquido_semestral = lucro_liquido_semestral[lucro_liquido_semestral != 0]

    
    df = pd.DataFrame(lucro_liquido_semestral, columns=["Net Income"])    
    df = df.infer_objects()
    
    df["Var"] = df["Net Income"].pct_change()

    var_media = df["Var"].mean()*100

    Lucro_liquido_futuro = df["Net Income"].iloc[-1] * (1 + var_media/100)

    num_papeis = ticker.info["sharesOutstanding"]
    LPA = Lucro_liquido_futuro / num_papeis
    payout = ticker.info["payoutRatio"] / 100
    dividendo_futuro = LPA * payout
    


    dataframes[empresa] = df

# Exibir os DataFrames criados
for empresa, df in dataframes.items():
    print(f"DataFrame para {empresa}:")
    print(df)
    print("=====================================") 

# preciso pegar o lucro líquido de todas as empresas, assim como o numero total de papeis e a média do payout

# Ver como o lucro liquido cresce e aplicar essa taxa para projetar o lucro nos proximos semestres e depois devidir pelo
# numero total de papeis do ativo, descobrindo o LPA, depois basta aplicar o payout e descobrir o dividendo por ação futuro,




